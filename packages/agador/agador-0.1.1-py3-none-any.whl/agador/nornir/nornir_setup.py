from typing import Optional
from decouple import config

from nornir import InitNornir
from nornir.core import Nornir

from ..credentials import update_nornir_credentials
from .logging import configure_nornir_logging, DEFAULT_LOGFILE
from .connection_options import configure_connection_options

CHUNK_SIZE = 5
NUM_WORKERS = 12


NETBOX_DEVICE_ROLES = [
    "av",
    "access-layer-switch",
    "bin",
    "core",
    "data-center",
    "distribution",
    "out-of-band",
    "security",
    "umd",
]

NETBOX_ILAB_DEVICE_ROLES = [
    "access",
    "agg",
    "bgw",
    "core",
    "data-center",
    "distribution",
    "legacy-bin",
    "legacy-core",
    "legacy-data-center",
    "legacy-distribution",
    "ngfw",
    "pe",
]


def nornir_setup(
    log_level: str = "DEBUG",
    log_globally: Optional[bool] = False,
    log_to_console: Optional[bool] = False,
    log_file: str = DEFAULT_LOGFILE,
    device_filter: Optional[str] = None,
    role_filter: Optional[str] = None,
) -> Nornir:
    """
    Initializes Nornir to point at netbox, and to only care about active
    devices tied to a specific subset of device roles.
    Sets up logging. Populates default and custom passwords from cyberark. Returns
    customized Nornir instance
    """

    configure_nornir_logging(log_level, log_globally, log_file, log_to_console)

    nb_url = config("NB_URL")

    filter_params = {"status": "active", "has_primary_ip": "True"}

    # Restrict what the netbox inventory plugin pulls if it was indicated
    # on the CLI
    if device_filter:
        filter_params["name"] = device_filter
    elif role_filter:
        filter_params["role"] = [role_filter]
    elif "ilab" in nb_url:
        filter_params["role"] = NETBOX_ILAB_DEVICE_ROLES
    else:
        filter_params["role"] = NETBOX_DEVICE_ROLES

    # Nornir initialization
    nr = InitNornir(
        runner={
            "plugin": "multiprocess",
            "options": {
                "num_workers": NUM_WORKERS,
            },
        },
        inventory={
            "plugin": "NetBoxInventory2",
            "options": {
                "nb_url": nb_url,
                "nb_token": config("NB_TOKEN"),
                "filter_parameters": filter_params,
                "ssl_verify": False,
            },
        },
        logging={
            "enabled": False,
        },
    )

    # rename virtual chassis devices (that have '_X' appended to their hostname)
    # to match the netbox VC name
    for host in nr.inventory.hosts.values():
        if host.data.get("virtual_chassis"):
            host.name = host.data["virtual_chassis"]["name"]

    update_nornir_credentials(nr, config("CYBERARK_ENV_FILE"))
    configure_connection_options(nr)

    return nr
