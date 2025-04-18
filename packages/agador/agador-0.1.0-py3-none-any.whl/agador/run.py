import sys
import re
import argparse
from datetime import datetime
import socket
import logging

from decouple import config

from agador.nornir import nornir_setup

from agador.nornir.tasks import process_device
from agador.nornir.processors import (
    AgadorProcessor,
    TraceFile,
)
from agador.utils import git_update, parse_command_map


logger = logging.getLogger(__name__)


def main():
    cmd_map = parse_command_map()

    parser = argparse.ArgumentParser(description="Run agador")

    filter_args = parser.add_mutually_exclusive_group()
    filter_args.add_argument(
        "--device", help="Restrict the update to a particular device"
    )
    filter_args.add_argument(
        "--role", help="Restrict the update to a specific netbox device role"
    )

    parser.add_argument(
        "--cmds",
        nargs="*",
        help="Limit update to a subset of tasks/commands",
        choices=cmd_map,
    )

    log_args = parser.add_mutually_exclusive_group()
    log_args.add_argument("-l", "--log-level", help="Set log level for agador only")
    log_args.add_argument("-L", "--LOG-LEVEL", help="set log level for all libraries")
    parser.add_argument("--echo", action="store_true", help="echo logfile to stdout")
    parser.add_argument("--trace", action="store_true", help="Save device session logs")

    args = parser.parse_args()

    if args.trace and not args.device:
        sure = input(
            "Trace output is for debugging only. Are you sure you want to save session logs for ALL devices (y/n)? "
        )
        if re.match(r"[Yy]", sure):
            print(f"Fine. Logs will be saved at {config('LOG_DIR')}")
        else:
            print("Good choice! Turning trace off.")
            args.trace = False

    if args.log_level:
        log_level = args.log_level
    elif args.LOG_LEVEL:
        log_level = args.LOG_LEVEL
    else:
        log_level = logging.INFO

    logger.info("initializing nornir")

    # initialize nornir
    nr = nornir_setup(
        log_level=log_level,
        log_globally=bool(args.LOG_LEVEL),
        log_to_console=args.echo,
        device_filter=args.device,
        role_filter=args.role,
    )

    logger.info(
        "Nornir initialization complete - inventory has %s items",
        len(nr.inventory.hosts.keys()),
    )

    if not (nr.inventory.hosts.keys()):
        logger.error("No matching hosts found in netbox inventory!")
        sys.exit(1)

    # run commands against all our devices
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_logfile = f"{config('LOG_DIR')}/results_{timestamp}"

    # setting up processors
    processors = [
        AgadorProcessor(len(nr.inventory.hosts), config("EMAIL_ADDRESS"), config("EMAIL_RECIPIENTS"), results_logfile, args.echo)
    ]
    if args.trace:
        processors.append(TraceFile(config("LOG_DIR")))

    logger.debug("Starting run...")
    nr.with_processors(processors).run(
        task=process_device,
        cmd_list=args.cmds,
        cmd_map=cmd_map,
        on_failed=True,
    )

    # add/commit/push git changes if applicable
    logger.debug("git updates")
    formatted_date = datetime.strftime(datetime.now(), "%a %d %b %Y, %I:%M%p")
    commit_msg = f"Agador backup from {socket.gethostname()} at {formatted_date}"

    for cmd, data in cmd_map.items():
        if not data.get("save_to_file"):
            continue
        if args.cmds and cmd not in args.cmds:
            continue
        git_update(data["save_to_file"]["destination"], commit_msg)

if __name__ == "__main__":
    main()