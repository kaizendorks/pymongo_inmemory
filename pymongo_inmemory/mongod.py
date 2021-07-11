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
            logger.warn("Using Mongod port set by user: {}".format(set_port))
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
        self._mongod_port = None
        self._mongod_ip = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

    def start(self):
        mongod_config = MongodConfig()
        self._mongod_port = mongod_config.port
        self._mongod_ip = mongod_config.local_address
        self.data_folder = TemporaryDirectory(prefix="pymongoim")

        while self.is_locked:
            logger.warn((
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
            "--port", self._mongod_port,
            "--bind_ip", self._mongod_ip,
            "--storageEngine", mongod_config.engine,
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
        if self._mongod_ip is not None and self._mongod_port is not None:
            return "mongodb://{host}:{port}".format(
                host=self._mongod_ip,
                port=self._mongod_port
            )
        else:
            return None

    @property
    def is_locked(self):
        return os.path.exists(os.path.join(self.data_folder.name, "mongod.lock"))

    @property
    def is_healthy(self):
        healthcheck = [
            os.path.join(self._bin_folder, "mongo"),
            self.connection_string,
            "--quiet",
            "--eval", "db.serverStatus().uptime"
        ]
        try:
            logger.debug("Getting status")
            uptime = subprocess.check_output(healthcheck)
        except subprocess.CalledProcessError:
            logger.debug("Status: Not running")
            return False
        else:
            if int(uptime) > 0:
                logger.debug("Status: Running for {up} secs".format(
                    up=str(uptime.decode()).strip()
                ))
                return True
            else:
                logger.debug("Status: Just started.")
                return False

    def mongodump(self, database, collection):
        dump_command = [
            os.path.join(self._bin_folder, "mongodump"),
            "--host", self._mongod_ip,
            "--port", self._mongod_port,
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
