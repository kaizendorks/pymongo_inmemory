from configparser import ConfigParser
import os
import socket


def find_open_port(sq):
    for port in sq:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            if 0 != soc.connect_ex(("localhost", port)):
                return port


DEFAULT_CONF = {
    "mongo_version": "4.0.10"
}


def _check_environment_vars(option, fallback=None):
    "Check if `option` is defined in environment variables"
    return os.environ.get("PYMONGOIM__{}".format(str(option).upper()), default=fallback)


def _check_cfg(option, filename, fallback=None):
    "Check if `option` is defined in `filename` ini file in the root folder"
    parser = ConfigParser()
    parser.read(filename)
    return parser.get(
        "pymongo_inmemory",
        option,
        fallback=fallback,
        raw=True
    )


def conf(option, fallback=None):
    """Retrieve asked `option` if possible. There are number of places that are checked.
    In the order of precedence,
    1. Environment variables
    2. setup.cfg in the root folder
    3. pymongo_inmemory.ini in the root folder
    4. `DEFAULT_CONF`

    Root folder is where the Python interpreter is invoked.

    Environment variables should be prefixed with `PYMONGOIM__`. For instance,
    `PYMONGOIM__DOWNLOAD_FOLDER`.

    Parameters
    ----------
    option: str
        Asked option

    Returns
    -------
    any or None: If there is a value, it'll return it otherwise it'll return `None`.
    """
    return _check_environment_vars(
        option,
        fallback=_check_cfg(
            option, "setup.cfg",
            fallback=_check_cfg(
                option, "pymongo_inmemory.ini",
                fallback=DEFAULT_CONF.get(option, fallback)
            )
        )
    )
