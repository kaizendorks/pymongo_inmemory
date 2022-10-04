"""MongoDB daemon process wrapper

This module can be used for spinning up an ephemeral MongoDB instance:
::
    python -m python_inmemory.mongod
"""
import atexit
import logging
import os
import signal
import subprocess
import time
import threading
from tempfile import TemporaryDirectory

import pymongo

from ._utils import conf, find_open_port
from .downloader import download

logger = logging.getLogger("PYMONGOIM_MONGOD")
# Holds references to open Popen objects which spawn MongoDB daemons.
_popen_objs = []


@atexit.register
def cleanup():
    logger.info("Cleaning created processes.")
    for o in _popen_objs:
        if o.poll() is None:
            logger.debug("Found {}".format(o.pid))
            o.terminate()


def clean_before_kill(signum, stack):
    logger.warning("Received kill signal.")
    cleanup()
    exit()


def _last_line(input, as_a=int):
    """Get the last line from given bytes

    TODO - Pull it to utils if needed elsewhere in the future.
    """
    lines = list(
        filter(
            lambda x: x, [
                x.strip().decode() for x in input.split(bytes(os.linesep, 'utf8'))
            ]
        )
    )
    return as_a(lines[-1])


# as per https://docs.python.org/3.6/library/signal.html#signals-and-threads
# only the main thread is allowed to set a new signal handler.
# This means that if this module is imported by a thread other than the
# main one it will raise an error.
if threading.current_thread() is threading.main_thread():
    signal.signal(signal.SIGTERM, clean_before_kill)


class MongodConfig:
    def __init__(self):
        self.local_address = "127.0.0.1"
        self.engine = "ephemeralForTest"

    @property
    def port(self):
        set_port = conf('mongod_port')
        if set_port is None:
            return str(find_open_port(range(27017, 28000)))
        else:
            logger.warning("Using Mongod port set by user: {}".format(set_port))
            return set_port


class Mongod:
    """Wrapper for MongoDB daemon instance. Can be used with context managers.
    During contruction it calls `download` function of `downloader` to get the
    defined MongoDB version.

    Daemon is managed by `subprocess.Popen`. all Popen objects are registered
    with `atexit` module to ensure clean up.
    """
    def __init__(self):
        logger.info("Checking binary")

        self._bin_folder = download()
        self._proc = None
        self._connection_string = None

        self.config = MongodConfig()
        self.data_folder = TemporaryDirectory(prefix="pymongoim")
        self._client = pymongo.MongoClient(self.connection_string)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

    def start(self):
        while self.is_locked:
            logger.warning((
                "Lock file found, possibly another mock server is running. "
                "Changing the data folder."
            ))
            self.data_folder = TemporaryDirectory(prefix="pymongoim")

        self.log_path = os.path.join(self.data_folder.name, "mongod.log")

        logger.info("Starting mongod with {cs}...".format(cs=self.connection_string))
        boot_command = [
            os.path.join(self._bin_folder, "mongod"),
            "--dbpath", self.data_folder.name,
            "--logpath", self.log_path,
            "--port", self.config.port,
            "--bind_ip", self.config.local_address,
            "--storageEngine", self.config.engine,
        ]
        logger.debug(boot_command)
        self._proc = subprocess.Popen(boot_command)
        _popen_objs.append(self._proc)
        while not self.is_healthy:
            pass
        logger.info("Started mongod.")
        logger.info("Connect with: {cs}".format(cs=self.connection_string))

    def stop(self):
        logger.info("Sending kill signal to mongod.")
        self._proc.terminate()
        while self._proc.poll() is None:
            logger.debug("Waiting for MongoD shutdown.")
            time.sleep(1)
        self.data_folder.cleanup()

    @property
    def connection_string(self):
        if self._connection_string is not None:
            return self._connection_string

        if (
            self.config.local_address is not None
            and self.config.port is not None
        ):
            self._connection_string = "mongodb://{host}:{port}".format(
                host=self.config.local_address,
                port=self.config.port
            )
        else:
            self._connection_string = None

        return self._connection_string

    @property
    def is_locked(self):
        return os.path.exists(os.path.join(self.data_folder.name, "mongod.lock"))

    @property
    def is_healthy(self):
        db = self._client["admin"]
        status = db.command("serverStatus")
        try:
            logger.debug("Getting status")
            uptime = int(status["uptime"])
        except subprocess.CalledProcessError:
            logger.debug("Status: Not running")
            return False
        else:
            if uptime > 0:
                version = status["version"]
                logger.debug(
                    "Status: MongoDB {} running for {} secs".format(version, uptime)
                )
                return True
            else:
                logger.debug("Status: Just started.")
                return False

    def mongodump(self, database, collection):
        dump_command = [
            os.path.join(self._bin_folder, "mongodump"),
            "--host", self.config.local_address,
            "--port", self.config.port,
            "--out", "-",
            "--db", database,
            "--collection", collection,
        ]
        proc = subprocess.run(dump_command, stdout=subprocess.PIPE)
        return proc.stdout

    def logs(self):
        with open(self.log_path, "r") as logfile:
            return logfile.readlines()


if __name__ == "__main__":
    # This part is used for integrity tests too.
    logging.basicConfig(level=logging.DEBUG)
    with Mongod() as md:
        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass
