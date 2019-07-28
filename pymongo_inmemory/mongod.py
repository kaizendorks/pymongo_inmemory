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
        self._proc = subprocess.Popen(self._boot)
        while not self.is_healthy():
            pass

    def stop(self):
        self._proc.terminate()

    def is_healthy(self):
        try:
            uptime = subprocess.check_output(self._healthcheck)
        except subprocess.CalledProcessError:
            return False
        else:
            if int(uptime) > 0:
                return True
            else:
                return False


if __name__ == "__main__":
    with Mongod() as md:
        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass
