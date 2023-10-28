import subprocess

from pymongo_inmemory.mongod import Mongod
import pymongo_inmemory.downloader as downloader
from pymongo_inmemory.context import Context


class Popen:
    def __init__(self, cmd):
        self.cmd = cmd
        self.terminated = False

    def terminate(self):
        self.terminated = True

    def poll(self):
        return True


def returns_true():
    return True


def download():
    return ""


def test_mongod_data_folder_config(monkeypatch):
    monkeypatch.setattr(subprocess, "Popen", Popen)
    monkeypatch.setattr(Mongod, "is_healthy", returns_true)
    monkeypatch.setattr(downloader, "download", download)

    monkeypatch.setenv("PYMONGOIM__MONGOD_DATA_FOLDER", "TEST")

    with Mongod(None) as md:
        assert md.data_folder == "TEST"


def test_dbname_config(monkeypatch):
    monkeypatch.setattr(subprocess, "Popen", Popen)
    monkeypatch.setattr(Mongod, "is_healthy", returns_true)
    monkeypatch.setattr(downloader, "download", download)

    monkeypatch.setenv("PYMONGOIM__DBNAME", "TEST")

    with Mongod(None) as md:
        assert md.config.connection_string.endswith("TEST")


def test_mongo_client_host_config(monkeypatch):
    monkeypatch.setattr(subprocess, "Popen", Popen)
    monkeypatch.setattr(Mongod, "is_healthy", returns_true)
    monkeypatch.setattr(downloader, "download", download)
    monkeypatch.setenv("PYMONGOIM__MONGO_CLIENT_HOST", "mongodb://test")

    with Mongod(None) as md:
        assert md.config.connection_string == "mongodb://test"
