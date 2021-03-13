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



def test_best_url():
    """
    - Given `major.minor.patch` version:
        - Starting from `major` to `patch`
        - If there is an exact match it should take it
        - If there isn't, it should take the highest and go on with the highest
    """
    url_tree = EXPECTED_TREE
    assert utools.best_url("linux") == EXPECTED_TREE[3][0][42]["linux"]["generic"], "OS is not given, should find Linux:Generic"
    assert utools.best_url("suse") == EXPECTED_TREE[3][0][42]["suse"]["2"], "OS is SuSE, should find latest SuSE"
    assert utools.best_url("amazon", "3") == EXPECTED_TREE[3][0][42]["amazon"]["3"], "Both OS and OS version exists, should find the URL."
    with pytest.raises(utools.OperatingSystemNameNotFound):
        utools.best_url("osx")
    with pytest.raises(utools.OperatingSystemVersionNotFound):
        utools.best_url("suse", "4")

    assert utools.best_url("suse") == EXPECTED_TREE[1][3][4]["suse"]["1"], "OS is SuSE, should find latest SuSE for that MongoDB version"
    assert utools.best_url("windows") == EXPECTED_TREE[1][3][4]["windows"]["generic"], "If only one version is there should give that version."
