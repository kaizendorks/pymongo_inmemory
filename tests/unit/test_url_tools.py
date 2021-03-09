from pprint import pprint

import pymongo_inmemory.downloader._url_tools as utools


FIXTURE = [
    ["1", "0", "1", "osx", "generic", "https://osx.generic/1.0.1"],
    ["1", "0", "1", "suse", "1", "https://suse.1/1.0.1"],
    ["1", "0", "1", "windows", "generic", "https://windows.generic/1.0.1"],
    ["1", "0", "1", "linux", "generic", "https://linux.generic/1.0.1"],
    ["1", "0", "1", "amazon", "3", "https://amazon.3/1.0.1"],
    ["1", "0", "1", "amazon", "4", "https://amazon.4/1.0.1"],

    ["1", "3", "4", "osx", "generic", "https://osx.generic/1.3.4"],
    ["1", "3", "4", "suse", "1", "https://suse.1/1.3.4"],
    ["1", "3", "4", "windows", "generic", "https://windows.generic/1.3.4"],
    ["1", "3", "4", "linux", "generic", "https://linux.generic/1.3.4"],
    ["1", "3", "4", "amazon", "3", "https://amazon.3/1.3.4"],
    ["1", "3", "4", "amazon", "4", "https://amazon.4/1.3.4"],

    ["3", "5", "6", "osx", "generic", "https://osx.generic/3.5.6"],
    ["3", "5", "6", "suse", "2", "https://suse.2/3.5.6"],
    ["3", "5", "6", "windows", "generic", "https://windows.generic/3.5.6"],
    ["3", "5", "6", "amazon", "3", "https://amazon.3/3.5.6"],
    ["3", "5", "6", "amazon", "4", "https://amazon.4/3.5.6"],

    ["3", "0", "42", "osx", "generic", "https://osx.generic/3.0.42"],
    ["3", "0", "42", "suse", "1", "https://suse.1/3.0.42"],
    ["3", "0", "42", "suse", "2", "https://suse.2/3.0.42"],
    ["3", "0", "42", "windows", "generic", "https://windows.generic/3.0.42"],
    ["3", "0", "42", "linux", "generic", "https://linux.generic/3.0.42"],
    ["3", "0", "42", "amazon", "3", "https://amazon.3/3.0.42"],
    ["3", "0", "42", "amazon", "4", "https://amazon.4/3.0.42"],

    ["4", "0", "0", "osx", "generic", "https://osx.generic/4.0.0"],
    ["4", "0", "0", "suse", "2", "https://suse.2/4.0.0"],
    ["4", "0", "0", "windows", "generic", "https://windows.generic/4.0.0"],
    ["4", "0", "0", "amazon", "3", "https://amazon.3/4.0.0"],
    ["4", "0", "0", "amazon", "4", "https://amazon.4/4.0.0"],
]


EXPECTED_TREE = {
    1: {
        0: {
            1: {
                "amazon": {
                    "3": "https://amazon.3/1.0.1",
                    "4": "https://amazon.4/1.0.1"
                },
                "linux": {
                    "generic": "https://linux.generic/1.0.1"
                },
                "suse": {
                    "1": "https://suse.1/1.0.1"
                },
                "windows": {
                    "generic": "https://windows.generic/1.0.1"
                }
            }
        },
        3: {
            4: {
                "amazon": {
                    "3": "https://amazon.3/1.3.4",
                    "4": "https://amazon.4/1.3.4"
                },
                "linux": {
                    "generic": "https://linux.generic/1.3.4"
                },
                "suse": {
                    "1": "https://suse.1/1.3.4"
                },
                "windows": {
                    "generic": "https://windows.generic/1.3.4"
                }
            }
        }
    },
    3: {
        0: {
            42: {
                "amazon": {
                    "3": "https://amazon.3/3.0.42",
                    "4": "https://amazon.4/3.0.42"
                },
                "linux": {
                    "generic": "https://linux.generic/3.0.42"
                },
                "suse": {
                    "1": "https://suse.1/3.0.42",
                    "2": "https://suse.2/3.0.42"
                },
                "windows": {
                    "generic": "https://windows.generic/3.0.42"
                }
            }
        },
        5: {
            6: {
                "amazon": {
                    "3": "https://amazon.3/3.5.6",
                    "4": "https://amazon.4/3.5.6"
                },
                "suse": {
                    "2": "https://suse.2/3.5.6"
                },
                "windows": {
                    "generic": "https://windows.generic/3.5.6"
                }
            }
        }
    },
    4: {
        0: {
            0: {
                "amazon": {
                    "3": "https://amazon.3/4.0.0",
                    "4": "https://amazon.4/4.0.0"
                },
                "suse": {
                    "2": "https://suse.2/4.0.0"
                },
                "windows": {
                    "generic": "https://windows.generic/4.0.0"
                }
            }
        }
    }
}


def test_make_url_tree():
    url_tree = utools.make_url_tree(FIXTURE)
    assert url_tree == EXPECTED_TREE


def test_closest_version_branch():
    url_tree = utools.make_url_tree(FIXTURE)
    assert utools._closest_version_branch(url_tree, 4, 0, 0) == EXPECTED_TREE[4][0][0]
    assert utools._closest_version_branch(url_tree, 4, 0, 6) == EXPECTED_TREE[4][0][0]
    assert utools._closest_version_branch(url_tree, 4, 5, 0) == EXPECTED_TREE[4][0][0]
    assert utools._closest_version_branch(url_tree, 4, 5, 42) == EXPECTED_TREE[4][0][0]
    assert utools._closest_version_branch(url_tree, 4) == EXPECTED_TREE[4][0][0]
    assert utools._closest_version_branch(url_tree, 3, 5, 42) == EXPECTED_TREE[3][5][6]
    assert utools._closest_version_branch(url_tree, 3, 5, 5) == EXPECTED_TREE[3][5][6]
    assert utools._closest_version_branch(url_tree, 3, 5) == EXPECTED_TREE[3][5][6]
    assert utools._closest_version_branch(url_tree, 3) == EXPECTED_TREE[3][5][6]
    assert utools._closest_version_branch(url_tree, 3, 0, 5) == EXPECTED_TREE[3][0][42]
    assert utools._closest_version_branch(url_tree, 3, 0) == EXPECTED_TREE[3][0][42]
    assert utools._closest_version_branch(url_tree, 1, 2, 0) == EXPECTED_TREE[1][3][4]
    assert utools._closest_version_branch(url_tree, 1) == EXPECTED_TREE[1][3][4]
    assert utools._closest_version_branch(url_tree) == EXPECTED_TREE[4][0][0]
