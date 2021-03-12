# flake8: noqa E501
from collections import namedtuple


class OperatingSystemNameNotFound(ValueError):
    pass


class OperatingSystemVersionNotFound(ValueError):
    pass


MajorMinor = namedtuple("MajorMinor", ["major", "minor"])

URLS = {
    2: {
        6: {
            "patches": list(range(13)),
            "os_names": {
                "windows": {
                    "generic": "https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-{}.zip",
                },
                "sunos": {
                    "5": "https://fastdl.mongodb.org/sunos5/mongodb-sunos5-x86_64-{}.tgz",
                },
                "osx": {
                    "generic": "https://fastdl.mongodb.org/osx/mongodb-osx-x86_64-{}.tgz",
                },
                "linux": {
                    "generic": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-{}.tgz",
                },
            },
        }
    },
    3: {
        0: {
            "patches": list(range(16)),
            "os_names": {
                "windows": {
                    "generic": "https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-{}.zip",
                },
                "ubuntu": {
                    "14": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1404-{}.tgz",
                    "12": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1204-{}.tgz",
                },
                "suse": {
                    "11": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse11-{}.tgz",
                },
                "sunos": {
                    "5": "https://fastdl.mongodb.org/sunos5/mongodb-sunos5-x86_64-{}.tgz",
                },
                "rhel": {
                    "5": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel55-{}.tgz",
                    "6": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel62-{}.tgz",
                    "7": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-{}.tgz",
                },
                "osx": {
                    "generic": "https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-{}.tgz",
                },
                "linux": {
                    "generic": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-{}.tgz",
                },
                "debian": {
                    "7": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian71-{}.tgz",
                },
                "amazon": {
                    "1": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon-{}.tgz",
                },
            },
        },
        2: {
            "patches": list(range(23)),
            "os_names": {
                "windows": {
                    "generic": "https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2008plus-{}.zip",
                },
                "ubuntu": {
                    "16": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1604-{}.tgz",
                    "14": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1404-{}.tgz",
                },
                "suse": {
                    "12": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse12-{}.tgz",
                },
                "rhel": {
                    "5": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel55-{}.tgz",
                    "6": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel62-{}.tgz",
                    "7": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-{}.tgz",
                },
                "osx": {
                    "generic": "https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-{}.tgz",
                },
                "linux": {
                    "generic": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-{}.tgz",
                },
                "debian": {
                    "8": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian81-{}.tgz",
                },
                "amazon": {
                    "1": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon-{}.tgz",
                },
            },
        },
        6: {
            "patches": list(range(23)),
            "os_names": {
                "windows": {
                    "generic": "https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2008plus-{}.zip",
                },
                "ubuntu": {
                    "18": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-{}.tgz",
                    "16": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1604-{}.tgz",
                    "14": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1404-{}.tgz",
                },
                "suse": {
                    "12": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse12-{}.tgz"
                },
                "rhel": {
                    "8": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel80-{}.tgz",
                    "6": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel62-{}.tgz",
                    "7": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-{}.tgz",
                },
                "osx": {
                    "generic": "https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-{}.tgz",
                },
                "linux": {
                    "generic": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-{}.tgz",
                },
                "debian": {
                    "8": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian81-{}.tgz",
                    "9": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian92-{}.tgz",
                },
                "amazon": {
                    "1": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon-{}.tgz",
                    "2": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon2-{}.tgz",
                },
            },
        },
    },
    4: {
        0: {
            "patches": list(range(24)),
            "os_names": {
                "windows": {
                    "generic": "https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2008plus-{}.zip",
                },
                "ubuntu": {
                    "18": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-{}.tgz",
                    "16": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1604-{}.tgz",
                    "14": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1404-{}.tgz",
                },
                "suse": {
                    "12": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse12-{}.tgz"
                },
                "rhel": {
                    "8": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel80-{}.tgz",
                    "6": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel62-{}.tgz",
                    "7": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-{}.tgz",
                },
                "osx": {
                    "generic": "https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-{}.tgz",
                },
                "linux": {
                    "generic": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-{}.tgz",
                },
                "debian": {
                    "8": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian81-{}.tgz",
                    "9": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian92-{}.tgz",
                },
                "amazon": {
                    "1": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon-{}.tgz",
                    "2": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon2-{}.tgz",
                },
            },
        },
        2: {
            "patches": list(range(4)) + list(range(5,13)),
            "os_names": {
                "windows": {
                    "generic": "https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2012plus-{}.zip",
                },
                "ubuntu": {
                    "18": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-{}.tgz",
                    "16": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1604-{}.tgz",
                },
                "suse": {
                    "15": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse15-{}.tgz",
                    "12": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse12-{}.tgz",
                },
                "rhel": {
                    "8": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel80-{}.tgz",
                    "6": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel62-{}.tgz",
                    "7": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-{}.tgz",
                },
                "osx": {
                    "generic": "https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-{}.tgz",
                },
                "linux": {
                    "generic": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-{}.tgz",
                },
                "debian": {
                    "9": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian92-{}.tgz",
                    "10": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian10-{}.tgz",
                },
                "amazon": {
                    "1": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon-{}.tgz",
                    "2": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon2-{}.tgz",
                },
            },
        },
        4: {
            "patches": list(range(5)),
            "os_names": {
                "windows": {
                    "generic": "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-{}.zip",
                },
                "ubuntu": {
                    "20": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2004-{}.tgz",
                    "18": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-{}.tgz",
                    "16": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1604-{}.tgz",
                },
                "suse": {
                    "15": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse15-{}.tgz",
                    "12": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse12-{}.tgz",
                },
                "rhel": {
                    "8": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel80-{}.tgz",
                    "6": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel62-{}.tgz",
                    "7": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-{}.tgz",
                },
                "osx": {
                    "generic": "https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-{}.tgz",
                },
                "debian": {
                    "9": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian92-{}.tgz",
                    "10": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian10-{}.tgz",
                },
                "amazon": {
                    "1": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon-{}.tgz",
                    "2": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon2-{}.tgz",
                },
            },
        },
    },
}

class URLChooser:
    pass
