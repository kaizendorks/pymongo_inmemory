import subprocess

from pymongo_inmemory.mongod import Mongod
import pymongo_inmemory.downloader as downloader
from pymongo_inmemory.context import Context

import pytest


def test_mongod(monkeypatch):
    def download():
        return ""

    def returns_true():
        return True

    class Popen:
        def __init__(self, cmd):
            self.cmd = cmd
            self.terminated = False

        def terminate(self):
            self.terminated = True

        def poll(self):
            return True

    monkeypatch.setattr(subprocess, "Popen", Popen)
    monkeypatch.setattr(Mongod, "is_healthy", returns_true)
    monkeypatch.setattr(downloader, "download", download)

    context = Context()
    context.mongod_data_folder = "TEST"

    with Mongod(None) as md:
        assert md.data_folder == "TEST"
