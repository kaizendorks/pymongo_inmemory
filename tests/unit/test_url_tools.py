# flake8: noqa E501

import pytest

import pymongo_inmemory.downloader._url_tools as utools


EXPECTED_TREE = {
    1: {
        0: {
            "patches": [0, 1, 2],
            "os_names": {
                "osx": {
                    "generic": "https://osx.generic/{}",
                },
                "suse": {
                    "1": "https://suse.1/{}",
                    "2": "https://suse.2/{}",
                },
                "amazon": {
                    "3": "https://amazon.3/{}",
                    "4": "https://amazon.4/{}",
                },
                "linux": {
                    "generic": "https://linux.generic/{}",
                },
            },
        },
    },
    2: {
        4: {
            "patches": [0, 1, 2, 4, 5, 6],
            "os_names": {
                "osx": {
                    "generic": "https://osx.generic/{}",
                },
                "suse": {
                    "2": "https://suse.2/{}",
                },
                "rhel": {
                    "7": "https://rhel.7/{}",
                    "6": "https://rhel.6/{}",
                },
                "amazon": {
                    "3": "https://amazon.3/{}",
                    "4": "https://amazon.4/{}",
                },
                "linux": {
                    "generic": "https://linux.generic/{}",
                },
            },
        },
        6: {
            "patches": [0, 1, 2, 3, 4, 5, 6, 7],
            "os_names": {
                "osx": {
                    "generic": "https://osx.generic/{}",
                },
                "suse": {
                    "2": "https://suse.2/{}",
                },
                "rhel": {
                    "7": "https://rhel.7/{}",
                    "6": "https://rhel.6/{}",
                },
                "amazon": {
                    "3": "https://amazon.3/{}",
                    "4": "https://amazon.4/{}",
                },
                "linux": {
                    "generic": "https://linux.generic/{}",
                },
            },
        },
    },
    3: {
        2: {
            "patches": [0, 1, 2],
            "os_names": {
                "osx": {
                    "generic": "https://macosx.generic/{}",
                },
                "suse": {
                    "2": "https://suse.2/{}",
                },
                "rhel": {
                    "7": "https://rhel.7/{}",
                    "6": "https://rhel.6/{}",
                },
                "amazon": {
                    "3": "https://amazon.3/{}",
                    "4": "https://amazon.4/{}",
                },
            },
        },
    },
    4: {
        0: {
            "patches": [0,],
            "os_names": {
                "osx": {
                    "generic": "https://macosx.generic/{}",
                },
                "suse": {
                    "2": "https://suse.2/{}",
                },
                "rhel": {
                    "8": "https://rhel.8/{}",
                    "7": "https://rhel.7/{}",
                    "6": "https://rhel.6/{}",
                },
                "amazon": {
                    "3": "https://amazon.3/{}",
                    "4": "https://amazon.4/{}",
                },
            },
        },
    },
}


