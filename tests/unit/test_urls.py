# flake8: noqa E501

import pytest

import pymongo_inmemory.downloader._urls as utools

def test_best_url():
    """
    - Given `major.minor.patch` version:
        - Starting from `major` to `patch`
        - If there is an exact match it should take it
        - If there isn't, it should take the highest and go on with the highest
    """
    assert utools.best_url("linux") == ("https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-4.0.28.tgz", "4.0.28"), "Should find latest MongoDB for Linux:Generic"
    assert utools.best_url("linux", "3") == ("https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.6.22.tgz", "3.6.22"), "Should find latest MongoDB 3 for Linux:Generic"
    assert utools.best_url("linux", "3.4") == ("https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.4.24.tgz", "3.4.24"), "Should find latest MongoDB 3.4 for Linux:Generic"
    assert utools.best_url("linux", "2.6.11") == ("https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-2.6.11.tgz", "2.6.11"), "Should find exact MongoDB 2.6.11 for Linux:Generic"

    assert utools.best_url("linux", "4.4.4") == ("https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-4.0.28.tgz", "4.0.28"), "Linux:Generic support ends at 4.0.28, higher versions default to this."

    assert utools.best_url("ubuntu") == ("https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2004-5.0.8.tgz", "5.0.8"), "Should find latest MongoDB for latest Ubuntu"
    assert utools.best_url("ubuntu", os_ver=18) == ("https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-5.0.8.tgz", "5.0.8"), "Should find latest MongoDB for Ubuntu 18"
    assert utools.best_url("ubuntu", os_ver="14", version="3.0.3") == ("https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1404-3.0.3.tgz", "3.0.3"), "Should find MongoDB 3.0.3 for Ubuntu 14"

    with pytest.raises(utools.OperatingSystemNameNotFound):
        utools.best_url("xubuntu", os_ver="14", version="3.0.3")

    with pytest.raises(utools.OperatingSystemVersionNotFound):
        utools.best_url("ubuntu", os_ver="10", version="3.0.3")

    assert utools.best_url("ubuntu", os_ver="14", version="1.4.4") == ("https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1404-4.0.28.tgz", "4.0.28"), "If major version is not there should find latest major version of MongoDB for Ubuntu 14"
    assert utools.best_url("ubuntu", os_ver="14", version="3.8.4") == ("https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1404-3.6.22.tgz", "3.6.22"), "If minor version is not there should find latest minor version of MongoDB for given major version, for Ubuntu 14"
    assert utools.best_url("ubuntu", os_ver="14", version="3.4.22") == ("https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1404-3.4.24.tgz", "3.4.24"), "If patch version is not there should find latest patch version of MongoDB for given major.minor version, for Ubuntu 14"
