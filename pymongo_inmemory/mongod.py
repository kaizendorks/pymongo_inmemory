"""MongoDB daemon process wrapper

This module can be used for spinning up an ephemeral MongoDB instance:
::
    python -m python_inmemory.mongod
"""
import atexit
import logging
import os
import subprocess

from ._utils import find_open_port
from .downloader import CACHE_FOLDER, bin_folder, download

# Holds references to open Popen objects which spawn MongoDB daemons.
_popen_objs = []


@atexit.register
def cleanup():
    for o in _popen_objs:
        if o.poll() is None:
            o.terminate()


class MongodConfig:
    def __init__(self):
        self.local_address = "127.0.0.1"
        self.engine = "ephemeralForTest"

    @property
    def data_folder(self):
        return os.path.join(CACHE_FOLDER, "data")

    @property
    def port(self):
        return str(find_open_port(range(27017, 28000)))


class Mongod:
    """Wrapper for MongoDB daemon instance. Can be used with context managers.
    During contruction it calls `download` function of `downloader` to get the
    defined MongoDB version.

    Daemon is managed by `subprocess.Popen`. all Popen objects are registered
    with `atexit` module to ensure clean up.
    """
    def __init__(self):
        self._logger = logging.getLogger("PYMONGOIM_MONGOD")

        self._logger.info("Checking binary")
        download()

        self._proc = None
        self._healthcheck = [
            os.path.join(bin_folder(), "mongo"),
            "--quiet",
            "--eval", "db.serverStatus().uptime"
        ]
        self._mongod_port = None
        self._mongod_ip = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

    def start(self):
        self._logger.info("Starting mongod...")
        mongod_config = MongodConfig()
        self._mongod_port = mongod_config.port
        self._mongod_ip = mongod_config.local_address
        boot_command = [
            os.path.join(bin_folder(), "mongod"),
            "--dbpath", mongod_config.data_folder,
            "--port", self._mongod_port,
            "--bind_ip", self._mongod_ip,
            "--storageEngine", mongod_config.engine,
        ]
        self._proc = subprocess.Popen(boot_command)
        _popen_objs.append(self._proc)
        while not self.is_healthy:
            pass
        self._logger.info("Started mongod.")
        self._logger.info("Connect with: {cs}".format(cs=self.connection_string))

    def stop(self):
        self._logger.info("Sending kill signal to mongod.")
        self._proc.terminate()

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
    def is_healthy(self):
        try:
            self._logger.debug("Getting status")
            uptime = subprocess.check_output(self._healthcheck)
        except subprocess.CalledProcessError:
            self._logger.debug("Status: Not running")
            return False
        else:
            if int(uptime) > 0:
                self._logger.debug("Status: Running for {up} secs".format(
                    up=str(uptime.decode()).strip()
                ))
                return True
            else:
                self._logger.debug("Status: Just started.")
                return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    with Mongod() as md:
        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass
