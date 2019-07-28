import logging
import os
import subprocess

from ._utils import find_open_port
from .downloader import CACHE_FOLDER, bin_folder, download

MONGOD_CONFIG = {
    "data_folder": os.path.join(CACHE_FOLDER, "data"),
    "port": find_open_port(range(27017, 28000)),
    "local_address": "127.0.0.1",
}


class Mongod:
    def __init__(self):
        self._logger = logging.getLogger("PYMONGOIM_MONGOD")

        self._logger.info("Checking binary")
        download()

        self._proc = None
        self._boot = [
            os.path.join(bin_folder(), "mongod"),
            "--dbpath", MONGOD_CONFIG["data_folder"],
            "--port", str(MONGOD_CONFIG["port"]),
            "--bind_ip", MONGOD_CONFIG["local_address"],
            "--storageEngine", "ephemeralForTest",
        ]
        self._healthcheck = [
            os.path.join(bin_folder(), "mongo"),
            "--quiet",
            "--eval", "db.serverStatus().uptime"
        ]
        self.connection_string = "mongodb://{host}:{port}".format(
            host=MONGOD_CONFIG['local_address'],
            port=MONGOD_CONFIG['port']
        )

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

    def start(self):
        self._logger.info("Starting mongod...")
        self._proc = subprocess.Popen(self._boot)
        while not self.is_healthy():
            pass
        self._logger.info("Started mongod.")

    def stop(self):
        self._logger.info("Sending kill signal to mongod.")
        self._proc.terminate()

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
