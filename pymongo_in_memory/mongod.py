import os
import signal
import subprocess
import sys
from time import sleep

import pymongo


MONGOD_PROC = None


def start():
    MONGOD_PROC = subprocess.Popen([
        "./.cache/bin/mongod",
        "--dbpath", "./.cache/data",
        "--port", "27017",
        "--bind_ip", "127.0.0.1",
        "--storageEngine", "ephemeralForTest",
    ])
    sys.stdout.flush()


def stop():
    os.kill(MONGOD_PROC.pid, signal.SIGKILL)


if __name__ == "__main__":
    start()
    client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    db = client["test"]
    sleep(60)
    stop()
