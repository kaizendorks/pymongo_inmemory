from collections import namedtuple
import logging
import socket


logger = logging.getLogger("PYMONGOIM_UTILS")

SemVer = namedtuple("SemVer", ["major", "minor", "patch"])


def find_open_port(sq):
    for port in sq:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            if 0 != soc.connect_ex(("localhost", port)):
                return port


def make_semver(version=None):
    if version is None:
        return SemVer(None, None, None)

    parts = [int(x) for x in version.split(".")]
    if len(parts) >= 3:
        major, minor, patch = parts[:3]
    elif len(parts) == 2:
        major, minor = parts
        patch = None
    elif len(parts) == 1:
        major = parts[0]
        minor = patch = None
    else:
        major = minor = patch = None

    return SemVer(major, minor, patch)
