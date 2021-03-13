# flake8: noqa E501
from collections import namedtuple
import logging

from .._utils import make_semver, SemVer


logger = logging.getLogger("PYMONGOIM_DOWNLOAD_URL")


class OperatingSystemNameNotFound(ValueError):
    pass


class OperatingSystemVersionNotFound(ValueError):
    pass


PATCHES = {
    "2.6": list(range(13)),
    "3.0": list(range(16)),
    "3.2": list(range(23)),
    "3.2-sunos5": list(range(15)),
    "3.4": list(range(8)) + list(range(9, 25)),
    "3.4-sunos5": list(range(6)),
    "3.6": list(range(23)),
    "4.0": list(range(24)),
    "4.2": list(range(4)) + list(range(5, 13)),
    "4.4": list(range(5)),
}

PATTERNS = {
    "windows32-x86_64": "https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-{}.zip",
    "windows-2008plus-ssl": "https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-{}.zip",
    "windows-2012plus": "https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2012plus-{}.zip",
    "windows-x86_64": "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-{}.zip",
    "sunos5": "https://fastdl.mongodb.org/sunos5/mongodb-sunos5-x86_64-{}.tgz",
    "osx": "https://fastdl.mongodb.org/osx/mongodb-osx-x86_64-{}.tgz",
    "osx-ssl": "https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-{}.tgz",
    "macos": "https://fastdl.mongodb.org/osx/mongodb-macos-x86_64-{}.tgz",
}

# OS based index is not the most compact one but it's the most handy one
# Because we are limited by the OS we are running on first, MongoDB version second
URLS = {
    "amazon": {
        "1": {
            3: {
                0: {
                    "patches": PATCHES["3.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon-{}.tgz",
                },
                2: {
                    "patches": PATCHES["3.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon-{}.tgz",
                },
                6: {
                    "patches": PATCHES["3.6"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon-{}.tgz",
                },
            },
            4: {
                0: {
                    "patches": PATCHES["4.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon-{}.tgz",
                },
                2: {
                    "patches": PATCHES["4.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon-{}.tgz",
                },
                4: {
                    "patches": PATCHES["4.4"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon-{}.tgz",
                },
            },
        },
        "2": {
            3: {
                6: {
                    "patches": PATCHES["3.6"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon2-{}.tgz",
                },
            },
            4: {
                0: {
                    "patches": PATCHES["4.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon2-{}.tgz",
                },
                2: {
                    "patches": PATCHES["4.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon2-{}.tgz",
                },
                4: {
                    "patches": PATCHES["4.4"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon2-{}.tgz",
                },
            },
        },
    },
    "debian": {
        "7": {
            3: {
                0: {
                    "patches": PATCHES["3.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian71-{}.tgz",
                },
            },
        },
        "8": {
            3: {
                2: {
                    "patches": PATCHES["3.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian81-{}.tgz",
                },
                6: {
                    "patches": PATCHES["3.6"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian81-{}.tgz",
                },
            },
            4: {
                0: {
                    "patches": PATCHES["4.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian81-{}.tgz",
                },
            },
        },
        "9": {
            3: {
                6: {
                    "patches": PATCHES["3.6"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian92-{}.tgz",
                },
            },
            4: {
                0: {
                    "patches": PATCHES["4.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian92-{}.tgz",
                },
                2: {
                    "patches": PATCHES["4.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian92-{}.tgz",
                },
                4: {
                    "patches": PATCHES["4.4"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian92-{}.tgz",
                },
            },
        },
        "10": {
            4: {
                2: {
                    "patches": PATCHES["4.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian10-{}.tgz"
                },
                4: {
                    "patches": PATCHES["4.4"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian10-{}.tgz"
                },
            },
        },
    },
    "rhel": {
        "5": {
            3: {
                0: {
                    "patches": PATCHES["3.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel55-{}.tgz",
                },
                2: {
                    "patches": PATCHES["3.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel55-{}.tgz",
                },
            },
        },
        "6": {
            3: {
                0: {
                    "patches": PATCHES["3.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel62-{}.tgz",
                },
                2: {
                    "patches": PATCHES["3.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel62-{}.tgz",
                },
                6: {
                    "patches": PATCHES["3.6"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel62-{}.tgz",
                },
            },
            4: {
                0: {
                    "patches": PATCHES["4.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel62-{}.tgz",
                },
                2: {
                    "patches": PATCHES["4.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel62-{}.tgz",
                },
                4: {
                    "patches": PATCHES["4.4"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel62-{}.tgz",
                },
            },
        },
        "7": {
            3: {
                0: {
                    "patches": PATCHES["3.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-{}.tgz",
                },
                2: {
                    "patches": PATCHES["3.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-{}.tgz",
                },
                6: {
                    "patches": PATCHES["3.6"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-{}.tgz",
                },
            },
            4: {
                0: {
                    "patches": PATCHES["4.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-{}.tgz",
                },
                2: {
                    "patches": PATCHES["4.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-{}.tgz",
                },
                4: {
                    "patches": PATCHES["4.4"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-{}.tgz",
                },
            },
        },
        "8": {
            3: {
                6: {
                    "patches": PATCHES["3.6"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel80-{}.tgz",
                },
            },
            4: {
                0: {
                    "patches": PATCHES["4.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel80-{}.tgz",
                },
                2: {
                    "patches": PATCHES["4.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel80-{}.tgz",
                },
                4: {
                    "patches": PATCHES["4.4"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel80-{}.tgz",
                },
            },
        },
    },
    "suse": {
        "11": {
            3: {
                0: {
                    "patches": PATCHES["3.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse11-{}.tgz",
                }
            }
        },
        "12": {
            3: {
                2: {
                    "patches": PATCHES["3.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse12-{}.tgz",
                },
                6: {
                    "patches": PATCHES["3.6"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse12-{}.tgz"
                },
            },
            4: {
                0: {
                    "patches": PATCHES["4.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse12-{}.tgz"
                },
                2: {
                    "patches": PATCHES["4.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse12-{}.tgz"
                },
                4: {
                    "patches": PATCHES["4.4"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse12-{}.tgz"
                },
            },
        },
        "15": {
            4: {
                2: {
                    "patches": PATCHES["4.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse15-{}.tgz",
                },
                4: {
                    "patches": PATCHES["4.4"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse15-{}.tgz",
                },
            },
        },
    },
    "ubuntu": {
        "12": {
            3: {
                0: {
                    "patches": PATCHES["3.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1204-{}.tgz",
                },
            },
        },
        "14": {
            3: {
                0: {
                    "patches": PATCHES["3.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1404-{}.tgz",
                },
                2: {
                    "patches": PATCHES["3.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1404-{}.tgz",
                },
                6: {
                    "patches": PATCHES["3.6"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1404-{}.tgz",
                },
            },
            4: {
                0: {
                    "patches": PATCHES["4.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1404-{}.tgz",
                },
            },
        },
        "16": {
            3: {
                2: {
                    "patches": PATCHES["3.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1604-{}.tgz",
                },
                6: {
                    "patches": PATCHES["3.6"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1604-{}.tgz",
                },
            },
            4: {
                0: {
                    "patches": PATCHES["4.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1604-{}.tgz",
                },
                2: {
                    "patches": PATCHES["4.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1604-{}.tgz",
                },
                4: {
                    "patches": PATCHES["4.4"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1604-{}.tgz",
                },
            },
        },
        "18": {
            3: {
                6: {
                    "patches": PATCHES["3.6"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-{}.tgz",
                },
            },
            4: {
                0: {
                    "patches": PATCHES["4.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-{}.tgz",
                },
                2: {
                    "patches": PATCHES["4.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-{}.tgz",
                },
                4: {
                    "patches": PATCHES["4.4"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-{}.tgz",
                },
            },
        },
        "20": {
            4: {
                4: {
                    "patches": PATCHES["4.4"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2004-{}.tgz",
                },
            },
        },
    },
    "linux": {
        "generic": {
            2: {
                6: {
                    "patches": PATCHES["2.6"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-{}.tgz",
                },
            },
            3: {
                0: {
                    "patches": PATCHES["3.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-{}.tgz",
                },
                2: {
                    "patches": PATCHES["3.2"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-{}.tgz",
                },
                6: {
                    "patches": PATCHES["3.6"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-{}.tgz",
                },
            },
            4: {
                0: {
                    "patches": PATCHES["4.0"],
                    "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-{}.tgz",
                },
            },
        },
    },
    "osx": {
        "generic": {
            2: {
                6: {
                    "patches": PATCHES["2.6"],
                    "url": PATTERNS["osx"],
                },
            },
            3: {
                0: {
                    "patches": PATCHES["3.0"],
                    "url": PATTERNS["osx"],
                },
                2: {
                    "patches": PATCHES["3.2"],
                    "url": PATTERNS["osx-ssl"],
                },
                4: {
                    "patches": PATCHES["3.4"],
                    "url": PATTERNS["osx-ssl"],
                },
                6: {
                    "patches": PATCHES["3.6"],
                    "url": PATTERNS["osx-ssl"],
                },
            },
            4: {
                0: {
                    "patches": PATCHES["4.0"],
                    "url": PATTERNS["osx-ssl"],
                },
                2: {
                    "patches": PATCHES["4.2"],
                    "url": PATTERNS["macos"],
                },
                4: {
                    "patches": PATCHES["4.4"],
                    "url": PATTERNS["macos"],
                },
            },
        },
    },
    "sunos": {
        "5": {
            2: {
                6: {
                    "patches": PATCHES["2.6"],
                    "url": PATTERNS["sunos5"],
                },
            },
            3: {
                0: {
                    "patches": PATCHES["3.0"],
                    "url": PATTERNS["sunos5"],
                },
                2: {
                    "patches": PATCHES["3.2-sunos5"],
                    "url": PATTERNS["sunos5"],
                },
                4: {
                    "patches": PATCHES["3.4-sunos5"],
                    "url": PATTERNS["sunos5"],
                },
            },
        },
    },
    "windows": {
        "generic": {
            2: {
                6: {
                    "patches": PATCHES["2.6"],
                    "url": PATTERNS["windows32-x86_64"]
                },
            },
            3: {
                0: {
                    "patches": PATCHES["3.0"],
                    "url": PATTERNS["windows-2008plus-ssl"]
                },
                2: {
                    "patches": PATCHES["3.2"],
                    "url": PATTERNS["windows-2008plus-ssl"]
                },
                4: {
                    "patches": PATCHES["3.4"],
                    "url": PATTERNS["windows-2008plus-ssl"]
                },
                6: {
                    "patches": PATCHES["3.6"],
                    "url": PATTERNS["windows-2008plus-ssl"]
                },
            },
            4: {
                0: {
                    "patches": PATCHES["4.0"],
                    "url": PATTERNS["windows-2008plus-ssl"]
                },
                2: {
                    "patches": PATCHES["4.2"],
                    "url": PATTERNS["windows-2012plus"]
                },
                4: {
                    "patches": PATCHES["4.4"],
                    "url": PATTERNS["windows-x86_64"]
                },
            },
        },
    },
}


def best_url(os_name, version=None, os_ver=None, url_tree=None):
    if url_tree is None:
        url_tree = URLS

    major, minor, patch = make_semver(version)
    if major not in url_tree.keys():
        major = max(url_tree.keys())
        minor = max(url_tree[major].keys())
        patch = max(url_tree[major][minor]["patches"])
    elif minor not in url_tree[major].keys():
        minor = max(url_tree[major].keys())
        patch = max(url_tree[major][minor]["patches"])
    elif patch not in url_tree[major][minor]["patches"]:
        patch = max(url_tree[major][minor]["patches"])

    logger.info("Requested MongoDB version {}, found version: {}.{}.{}".format(
        version, major, minor, patch
    ))
    version = "{}.{}.{}".format(major, minor, patch)

    os_branch = url_tree[major][minor]
    os_ver = str(os_ver)
    os_name = str(os_name)

    if os_name not in os_branch.keys():
        raise OperatingSystemNameNotFound(
            "Can't find a MongoDB {} for {} for this version".format(version, os_name))

    if os_ver not in os_branch[os_name].keys():
        raise OperatingSystemVersionNotFound(
            "Can't find a MongoDB {} for {} {}, available OS versions: {}".format(
                version, os_name, os_ver, os_branch.keys()))

    return os_branch[os_name][os_ver].format(version)




