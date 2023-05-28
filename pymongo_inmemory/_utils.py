from collections import namedtuple
import logging
import socket
import os
from os import path

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


def mkdir_ifnot_exist(*folders):
    current_path = path.join(folders[0])
    if not path.isdir(current_path):
        os.mkdir(current_path)
    for x in folders[1:]:
        current_path = path.join(current_path, x)
        if not path.isdir(current_path):
            os.mkdir(current_path)
    return current_path
