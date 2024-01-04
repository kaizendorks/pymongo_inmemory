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

from ._utils import find_open_port
from .downloader import download
from .context import Context

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


# as per https://docs.python.org/3.6/library/signal.html#signals-and-threads
# only the main thread is allowed to set a new signal handler.
# This means that if this module is imported by a thread other than the
# main one it will raise an error.
if threading.current_thread() is threading.main_thread():
    signal.signal(signal.SIGTERM, clean_before_kill)


class MongodConfig:
    def __init__(self, pim_context: Context):
        self._pim_context = pim_context
        self.local_address = "127.0.0.1"
        self.engine = pim_context.storage_engine

    @property
    def port(self):
        set_port = self._pim_context.mongod_port
        if set_port is None:
            return str(find_open_port(range(27017, 28000)))
        else:
            return set_port

    @property
    def connection_string(self):
        if self._pim_context.mongo_client_host is not None:
            if self._pim_context.mongo_client_host.startswith("mongodb://"):
                return self._pim_context.mongo_client_host
            else:
                self.local_address = self._pim_context.mongo_client_host

        if self.local_address is not None and self.port is not None:
            if self._pim_context.dbname is None:
                return "mongodb://{host}:{port}".format(
                    host=self.local_address, port=self.port
                )
            else:
                return "mongodb://{host}:{port}/{dbname}".format(
                    host=self.local_address,
                    port=self.port,
                    dbname=self._pim_context.dbname,
                )


class Mongod:
    """Wrapper for MongoDB daemon instance. Can be used with context managers.
    During contruction it calls `download` function of `downloader` to get the
    defined MongoDB version.

    Daemon is managed by `subprocess.Popen`. all Popen objects are registered
    with `atexit` module to ensure clean up.
    """

    def __init__(self, pim_context: Context):
        self._pim_context = Context() if pim_context is None else pim_context
        logger.info("Running MongoD in the following context")
        logger.info(self._pim_context)

        logger.info("Checking binary")
        if self._pim_context.use_local_mongod:
            logger.warn("Using local mongod instance")
            self._bin_folder = ""
        else:
            self._bin_folder = download(self._pim_context)

        self._proc = None
        self._connection_string = None

        self.config = MongodConfig(self._pim_context)

        self._temp_data_folder = TemporaryDirectory(prefix="pymongoim")
        self._using_tmp_folder = self._pim_context.mongod_data_folder is None

        self._client = pymongo.MongoClient(self.connection_string)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

    def start(self):
        self._check_lock()
        self.log_path = os.path.join(self.data_folder, "mongod.log")

        logger.info("Starting mongod with {cs}...".format(cs=self.connection_string))
        boot_command = [
            os.path.join(self._bin_folder, "mongod"),
            "--dbpath",
            self.data_folder,
            "--logpath",
            self.log_path,
            "--port",
            self.config.port,
            "--bind_ip",
            self.config.local_address,
            "--storageEngine",
            self.config.engine,
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
        self._clean_up()

    @property
    def data_folder(self):
        if self._using_tmp_folder:
            return self._temp_data_folder.name
        else:
            return self._pim_context.mongod_data_folder

    @property
    def connection_string(self):
        if self._connection_string is not None:
            return self._connection_string

        self._connection_string = (
            self.config.connection_string
            if self.config.connection_string is not None
            else None
        )

        return self._connection_string

    @property
    def is_locked(self):
        return os.path.exists(os.path.join(self.data_folder, "mongod.lock"))

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
            "--host",
            self.config.local_address,
            "--port",
            self.config.port,
            "--out",
            "-",
            "--db",
            database,
            "--collection",
            collection,
        ]
        proc = subprocess.run(dump_command, stdout=subprocess.PIPE)
        return proc.stdout

    def logs(self):
        with open(self.log_path, "r") as logfile:
            return logfile.readlines()

    def _clean_up(self):
        if self._using_tmp_folder:
            self._temp_data_folder.cleanup()

    def _check_lock(self):
        while self.is_locked:
            if self._using_tmp_folder:
                raise RuntimeError(
                    (
                        "There is a lock file in the provided data folder. "
                        "Make sure that no other MongoDB is running."
                    )
                )
            logger.warning(
                (
                    "Lock file found, possibly another mock server is running. "
                    "Changing the data folder."
                )
            )
            self._temp_data_folder = TemporaryDirectory(prefix="pymongoim")


if __name__ == "__main__":
    # This part is used for integrity tests too.
    logging.basicConfig(level=logging.DEBUG)
    context = Context()
    with Mongod(context) as md:
        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass
