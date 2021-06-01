PATCH_RANGE = {
    "2.6": list(range(13)),
    "3.0": list(range(16)),
    "3.2": list(range(23)),
    "3.2-suse11": list(range(20)),
    "3.2-ubuntu18": list(range(20, 23)),
    "3.2-ubuntu16": list(range(7, 23)),
    "3.2-ubuntu12": list(range(20)),
    "3.2-sunos5": list(range(15)),
    "3.2-debian8": list(range(8, 23)),
    "3.2-debian7": list(range(21)),
    "3.4": list(range(8)) + list(range(9, 25)),
    "3.4-suse11": list(range(8)) + list(range(9, 15)),
    "3.4-ubuntu14": list(range(8)) + list(range(9, 21)) + list(range(23, 25)),
    "3.4-ubuntu12": list(range(8)) + list(range(9, 15)),
    "3.4-sunos5": list(range(6)),
    "3.4-debian7": list(range(8)) + list(range(9, 16)),
    "3.6": list(range(23)),
    "3.6-suse11": list(range(3)),
    "3.6-ubuntu18": list(range(20, 23)),
    "3.6-ubuntu14": list(range(13)) + list(range(14, 23)),
    "3.6-ubuntu12": list(range(4)),
    "3.6-rhel8": list(range(17, 23)),
    "3.6-debian9": list(range(5, 23)),
    "3.6-debian7": list(range(6)),
    "3.6-amazon2": [22],
    "4.0": list(range(24)),
    "4.0-rhel8": list(range(14, 24)),
    "4.0-ubuntu14": list(range(10)) + list(range(12, 24)),
    "4.0-ubuntu18": list(range(1, 24)),
    "4.2": list(range(4)) + list(range(5, 13)),
    "4.2-suse15": list(range(1, 4)) + list(range(5, 13)),
    "4.2-rhel8": list(range(1, 4)) + list(range(5, 13)),
    "4.2-debian10": list(range(1, 4)) + list(range(5, 13)),
    "4.4": list(range(7)),
}

PATTERNS = {
    "windows32-x86_64": "https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-{}.zip",
    "windows-2008plus-ssl": "https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-{}.zip",  # noqa E501
    "windows-2012plus": "https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2012plus-{}.zip",  # noqa E501
    "windows-x86_64": "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-{}.zip",
    "sunos5": "https://fastdl.mongodb.org/sunos5/mongodb-sunos5-x86_64-{}.tgz",
    "osx": "https://fastdl.mongodb.org/osx/mongodb-osx-x86_64-{}.tgz",
    "osx-ssl": "https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-{}.tgz",
    "macos": "https://fastdl.mongodb.org/osx/mongodb-macos-x86_64-{}.tgz",
    "linux": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-{}.tgz",
    "ubuntu20": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2004-{}.tgz",  # noqa E501
    "ubuntu18": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-{}.tgz",  # noqa E501
    "ubuntu16": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1604-{}.tgz",  # noqa E501
    "ubuntu14": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1404-{}.tgz",  # noqa E501
    "ubuntu12": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1204-{}.tgz",  # noqa E501
    "suse15": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse15-{}.tgz",
    "suse12": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse12-{}.tgz",
    "suse11": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse11-{}.tgz",
    "rhel8": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel80-{}.tgz",
    "rhel7": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-{}.tgz",
    "rhel6": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel62-{}.tgz",
    "rhel5": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel55-{}.tgz",
    "debian10": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian10-{}.tgz",
    "debian9": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian92-{}.tgz",
    "debian8": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian81-{}.tgz",
    "debian7": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian71-{}.tgz",
    "amazon2": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon2-{}.tgz",
    "amazon1": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon-{}.tgz",
}

# An index of URL patterns and patch ranges. First with OS and second with MongoDB
# version, because we are limited by the OS we are running on first, MongoDB
# version second.
URLS = {
    "amazon": {
        "1": {
            3: {
                0: {
                    "patches": PATCH_RANGE["3.0"],
                    "url": PATTERNS["amazon1"],
                },
                2: {
                    "patches": PATCH_RANGE["3.2"],
                    "url": PATTERNS["amazon1"],
                },
                4: {
                    "patches": PATCH_RANGE["3.4"],
                    "url": PATTERNS["amazon1"],
                },
                6: {
                    "patches": PATCH_RANGE["3.6"],
                    "url": PATTERNS["amazon1"],
                },
            },
            4: {
                0: {
                    "patches": PATCH_RANGE["4.0"],
                    "url": PATTERNS["amazon1"],
                },
                2: {
                    "patches": PATCH_RANGE["4.2"],
                    "url": PATTERNS["amazon1"],
                },
                4: {
                    "patches": PATCH_RANGE["4.4"],
                    "url": PATTERNS["amazon1"],
                },
            },
        },
        "2": {
            3: {
                6: {
                    "patches": PATCH_RANGE["3.6-amazon2"],
                    "url": PATTERNS["amazon2"],
                },
            },
            4: {
                0: {
                    "patches": PATCH_RANGE["4.0"],
                    "url": PATTERNS["amazon2"],
                },
                2: {
                    "patches": PATCH_RANGE["4.2"],
                    "url": PATTERNS["amazon2"],
                },
                4: {
                    "patches": PATCH_RANGE["4.4"],
                    "url": PATTERNS["amazon2"],
                },
            },
        },
    },
    "debian": {
        "7": {
            3: {
                0: {
                    "patches": PATCH_RANGE["3.0"],
                    "url": PATTERNS["debian7"],
                },
                2: {
                    "patches": PATCH_RANGE["3.2-debian7"],
                    "url": PATTERNS["debian7"],
                },
                4: {
                    "patches": PATCH_RANGE["3.4-debian7"],
                    "url": PATTERNS["debian7"],
                },
                6: {
                    "patches": PATCH_RANGE["3.6-debian7"],
                    "url": PATTERNS["debian7"],
                },
            },
        },
        "8": {
            3: {
                2: {
                    "patches": PATCH_RANGE["3.2-debian8"],
                    "url": PATTERNS["debian8"],
                },
                4: {
                    "patches": PATCH_RANGE["3.4"],
                    "url": PATTERNS["debian8"],
                },
                6: {
                    "patches": PATCH_RANGE["3.6"],
                    "url": PATTERNS["debian8"],
                },
            },
            4: {
                0: {
                    "patches": PATCH_RANGE["4.0"],
                    "url": PATTERNS["debian8"],
                },
            },
        },
        "9": {
            3: {
                6: {
                    "patches": PATCH_RANGE["3.6-debian9"],
                    "url": PATTERNS["debian9"],
                },
            },
            4: {
                0: {
                    "patches": PATCH_RANGE["4.0"],
                    "url": PATTERNS["debian9"],
                },
                2: {
                    "patches": PATCH_RANGE["4.2"],
                    "url": PATTERNS["debian9"],
                },
                4: {
                    "patches": PATCH_RANGE["4.4"],
                    "url": PATTERNS["debian9"],
                },
            },
        },
        "10": {
            4: {
                2: {
                    "patches": PATCH_RANGE["4.2-debian10"],
                    "url": PATTERNS["debian10"],
                },
                4: {
                    "patches": PATCH_RANGE["4.4"],
                    "url": PATTERNS["debian10"],
                },
            },
        },
    },
    "rhel": {
        "5": {
            3: {
                0: {
                    "patches": PATCH_RANGE["3.0"],
                    "url": PATTERNS["rhel5"],
                },
                2: {
                    "patches": PATCH_RANGE["3.2"],
                    "url": PATTERNS["rhel5"],
                },
            },
        },
        "6": {
            3: {
                0: {
                    "patches": PATCH_RANGE["3.0"],
                    "url": PATTERNS["rhel6"],
                },
                2: {
                    "patches": PATCH_RANGE["3.2"],
                    "url": PATTERNS["rhel6"],
                },
                4: {
                    "patches": PATCH_RANGE["3.4"],
                    "url": PATTERNS["rhel6"],
                },
                6: {
                    "patches": PATCH_RANGE["3.6"],
                    "url": PATTERNS["rhel6"],
                },
            },
            4: {
                0: {
                    "patches": PATCH_RANGE["4.0"],
                    "url": PATTERNS["rhel6"],
                },
                2: {
                    "patches": PATCH_RANGE["4.2"],
                    "url": PATTERNS["rhel6"],
                },
                4: {
                    "patches": PATCH_RANGE["4.4"],
                    "url": PATTERNS["rhel6"],
                },
            },
        },
        "7": {
            3: {
                0: {
                    "patches": PATCH_RANGE["3.0"],
                    "url": PATTERNS["rhel7"],
                },
                2: {
                    "patches": PATCH_RANGE["3.2"],
                    "url": PATTERNS["rhel7"],
                },
                4: {
                    "patches": PATCH_RANGE["3.4"],
                    "url": PATTERNS["rhel7"],
                },
                6: {
                    "patches": PATCH_RANGE["3.6"],
                    "url": PATTERNS["rhel7"],
                },
            },
            4: {
                0: {
                    "patches": PATCH_RANGE["4.0"],
                    "url": PATTERNS["rhel7"],
                },
                2: {
                    "patches": PATCH_RANGE["4.2"],
                    "url": PATTERNS["rhel7"],
                },
                4: {
                    "patches": PATCH_RANGE["4.4"],
                    "url": PATTERNS["rhel7"],
                },
            },
        },
        "8": {
            3: {
                6: {
                    "patches": PATCH_RANGE["3.6-rhel8"],
                    "url": PATTERNS["rhel8"],
                },
            },
            4: {
                0: {
                    "patches": PATCH_RANGE["4.0-rhel8"],
                    "url": PATTERNS["rhel8"],
                },
                2: {
                    "patches": PATCH_RANGE["4.2-rhel8"],
                    "url": PATTERNS["rhel8"],
                },
                4: {
                    "patches": PATCH_RANGE["4.4"],
                    "url": PATTERNS["rhel8"],
                },
            },
        },
    },
    "suse": {
        "11": {
            3: {
                0: {
                    "patches": PATCH_RANGE["3.0"],
                    "url": PATTERNS["suse11"],
                },
                2: {
                    "patches": PATCH_RANGE["3.2-suse11"],
                    "url": PATTERNS["suse11"],
                },
                4: {
                    "patches": PATCH_RANGE["3.4-suse11"],
                    "url": PATTERNS["suse11"],
                },
                6: {
                    "patches": PATCH_RANGE["3.6-suse11"],
                    "url": PATTERNS["suse11"],
                },
            },
        },
        "12": {
            3: {
                2: {
                    "patches": PATCH_RANGE["3.2"],
                    "url": PATTERNS["suse12"],
                },
                4: {
                    "patches": PATCH_RANGE["3.4"],
                    "url": PATTERNS["suse12"],
                },
                6: {
                    "patches": PATCH_RANGE["3.6"],
                    "url": PATTERNS["suse12"],
                },
            },
            4: {
                0: {
                    "patches": PATCH_RANGE["4.0"],
                    "url": PATTERNS["suse12"],
                },
                2: {
                    "patches": PATCH_RANGE["4.2"],
                    "url": PATTERNS["suse12"],
                },
                4: {
                    "patches": PATCH_RANGE["4.4"],
                    "url": PATTERNS["suse12"],
                },
            },
        },
        "15": {
            4: {
                2: {
                    "patches": PATCH_RANGE["4.2-suse15"],
                    "url": PATTERNS["suse15"],
                },
                4: {
                    "patches": PATCH_RANGE["4.4"],
                    "url": PATTERNS["suse15"],
                },
            },
        },
    },
    "ubuntu": {
        "12": {
            3: {
                0: {
                    "patches": PATCH_RANGE["3.0"],
                    "url": PATTERNS["ubuntu12"],
                },
                2: {
                    "patches": PATCH_RANGE["3.2-ubuntu12"],
                    "url": PATTERNS["ubuntu12"],
                },
                4: {
                    "patches": PATCH_RANGE["3.4-ubuntu12"],
                    "url": PATTERNS["ubuntu12"],
                },
                6: {
                    "patches": PATCH_RANGE["3.6-ubuntu12"],
                    "url": PATTERNS["ubuntu12"],
                },
            },
        },
        "14": {
            3: {
                0: {
                    "patches": PATCH_RANGE["3.0"],
                    "url": PATTERNS["ubuntu14"],
                },
                2: {
                    "patches": PATCH_RANGE["3.2"],
                    "url": PATTERNS["ubuntu14"],
                },
                4: {
                    "patches": PATCH_RANGE["3.4-ubuntu14"],
                    "url": PATTERNS["ubuntu14"],
                },
                6: {
                    "patches": PATCH_RANGE["3.6-ubuntu14"],
                    "url": PATTERNS["ubuntu14"],
                },
            },
            4: {
                0: {
                    "patches": PATCH_RANGE["4.0-ubuntu14"],
                    "url": PATTERNS["ubuntu14"],
                },
            },
        },
        "16": {
            3: {
                2: {
                    "patches": PATCH_RANGE["3.2-ubuntu16"],
                    "url": PATTERNS["ubuntu16"],
                },
                4: {
                    "patches": PATCH_RANGE["3.4"],
                    "url": PATTERNS["ubuntu16"],
                },
                6: {
                    "patches": PATCH_RANGE["3.6"],
                    "url": PATTERNS["ubuntu16"],
                },
            },
            4: {
                0: {
                    "patches": PATCH_RANGE["4.0"],
                    "url": PATTERNS["ubuntu16"],
                },
                2: {
                    "patches": PATCH_RANGE["4.2"],
                    "url": PATTERNS["ubuntu16"],
                },
                4: {
                    "patches": PATCH_RANGE["4.4"],
                    "url": PATTERNS["ubuntu16"],
                },
            },
        },
        "18": {
            3: {
                6: {
                    "patches": PATCH_RANGE["3.6-ubuntu18"],
                    "url": PATTERNS["ubuntu18"],
                },
            },
            4: {
                0: {
                    "patches": PATCH_RANGE["4.0-ubuntu18"],
                    "url": PATTERNS["ubuntu18"],
                },
                2: {
                    "patches": PATCH_RANGE["4.2"],
                    "url": PATTERNS["ubuntu18"],
                },
                4: {
                    "patches": PATCH_RANGE["4.4"],
                    "url": PATTERNS["ubuntu18"],
                },
            },
        },
        "20": {
            4: {
                4: {
                    "patches": PATCH_RANGE["4.4"],
                    "url": PATTERNS["ubuntu20"],
                },
            },
        },
    },
    "linux": {
        "generic": {
            2: {
                6: {
                    "patches": PATCH_RANGE["2.6"],
                    "url": PATTERNS["linux"],
                },
            },
            3: {
                0: {
                    "patches": PATCH_RANGE["3.0"],
                    "url": PATTERNS["linux"],
                },
                2: {
                    "patches": PATCH_RANGE["3.2"],
                    "url": PATTERNS["linux"],
                },
                4: {
                    "patches": PATCH_RANGE["3.4"],
                    "url": PATTERNS["linux"],
                },
                6: {
                    "patches": PATCH_RANGE["3.6"],
                    "url": PATTERNS["linux"],
                },
            },
            4: {
                0: {
                    "patches": PATCH_RANGE["4.0"],
                    "url": PATTERNS["linux"],
                },
            },
        },
    },
    "osx": {
        "generic": {
            2: {
                6: {
                    "patches": PATCH_RANGE["2.6"],
                    "url": PATTERNS["osx"],
                },
            },
            3: {
                0: {
                    "patches": PATCH_RANGE["3.0"],
                    "url": PATTERNS["osx"],
                },
                2: {
                    "patches": PATCH_RANGE["3.2"],
                    "url": PATTERNS["osx-ssl"],
                },
                4: {
                    "patches": PATCH_RANGE["3.4"],
                    "url": PATTERNS["osx-ssl"],
                },
                6: {
                    "patches": PATCH_RANGE["3.6"],
                    "url": PATTERNS["osx-ssl"],
                },
            },
            4: {
                0: {
                    "patches": PATCH_RANGE["4.0"],
                    "url": PATTERNS["osx-ssl"],
                },
                2: {
                    "patches": PATCH_RANGE["4.2"],
                    "url": PATTERNS["macos"],
                },
                4: {
                    "patches": PATCH_RANGE["4.4"],
                    "url": PATTERNS["macos"],
                },
            },
        },
    },
    "sunos": {
        "5": {
            2: {
                6: {
                    "patches": PATCH_RANGE["2.6"],
                    "url": PATTERNS["sunos5"],
                },
            },
            3: {
                0: {
                    "patches": PATCH_RANGE["3.0"],
                    "url": PATTERNS["sunos5"],
                },
                2: {
                    "patches": PATCH_RANGE["3.2-sunos5"],
                    "url": PATTERNS["sunos5"],
                },
                4: {
                    "patches": PATCH_RANGE["3.4-sunos5"],
                    "url": PATTERNS["sunos5"],
                },
            },
        },
    },
    "windows": {
        "generic": {
            2: {
                6: {
                    "patches": PATCH_RANGE["2.6"],
                    "url": PATTERNS["windows32-x86_64"]
                },
            },
            3: {
                0: {
                    "patches": PATCH_RANGE["3.0"],
                    "url": PATTERNS["windows-2008plus-ssl"]
                },
                2: {
                    "patches": PATCH_RANGE["3.2"],
                    "url": PATTERNS["windows-2008plus-ssl"]
                },
                4: {
                    "patches": PATCH_RANGE["3.4"],
                    "url": PATTERNS["windows-2008plus-ssl"]
                },
                6: {
                    "patches": PATCH_RANGE["3.6"],
                    "url": PATTERNS["windows-2008plus-ssl"]
                },
            },
            4: {
                0: {
                    "patches": PATCH_RANGE["4.0"],
                    "url": PATTERNS["windows-2008plus-ssl"]
                },
                2: {
                    "patches": PATCH_RANGE["4.2"],
                    "url": PATTERNS["windows-2012plus"]
                },
                4: {
                    "patches": PATCH_RANGE["4.4"],
                    "url": PATTERNS["windows-x86_64"]
                },
            },
        },
    },
}
