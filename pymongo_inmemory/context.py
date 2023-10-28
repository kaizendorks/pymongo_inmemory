from configparser import ConfigParser
import hashlib
import logging
import os
from os import path
import platform

from ._utils import mkdir_ifnot_exist
from .downloader._urls import best_url

DEFAULT_CONF = {}
CACHE_FOLDER = path.join(path.dirname(__file__), "..", ".cache")

logger = logging.getLogger("PYMONGOIM_UTILS")


class OperatingSystemNotFound(ValueError):
    pass


def _coercion(constructor, value):
    if constructor == bool:
        return value == "True"
    else:
        return constructor(value)


def _check_environment_vars(option, fallback=None):
    "Check if `option` is defined in environment variables"
    return os.environ.get("PYMONGOIM__{}".format(str(option).upper()), default=fallback)


def _check_cfg(option, filename, fallback=None):
    "Check if `option` is defined in `filename` ini file in the root folder"
    parser = ConfigParser()
    parser.read(filename)
    return parser.get("pymongo_inmemory", option, fallback=fallback, raw=True)


def conf(option, fallback=None, optional=True, coerce_with=str):
    """Retrieve asked `option` if possible. There are number of places that are checked.
    In the order of precedence,
    1. Environment variables
    2. setup.cfg in the root folder
    3. pymongo_inmemory.ini in the root folder
    4. `DEFAULT_CONF`

    Root folder is where the Python interpreter is invoked.

    Environment variables should be prefixed with `PYMONGOIM__`. For instance,
    `PYMONGOIM__DOWNLOAD_FOLDER`.

    Parameters
    ----------
    option: str
        Asked option

    Returns
    -------
    any or None: If there is a value, it'll return it otherwise it'll return `None`.
    """
    value = _check_environment_vars(
        option,
        fallback=_check_cfg(
            option,
            "setup.cfg",
            fallback=_check_cfg(
                option,
                "pymongo_inmemory.ini",
                fallback=DEFAULT_CONF.get(option, fallback),
            ),
        ),
    )

    if value is None:
        if not optional:
            raise ValueError(
                (
                    "Can't determine the value of {} "
                    "and it is not an optional parameter."
                ).format(option)
            )
    else:
        try:
            value = _coercion(coerce_with, value)
        except ValueError:
            value = None
        except Exception:
            raise ValueError(
                ("Can't coerce the value of {} to type {}").format(
                    option, coerce_with.__qualname__
                )
            )

    logger.debug("Value for {}=={}".format(option, value))

    return value


class Context:
    def __init__(
        self, os_name=None, version=None, os_ver=None, ignore_cache=False
    ) -> None:
        self.mongo_version = conf("mongo_version", version)
        self.mongod_port = conf("mongod_port", None, coerce_with=int)
        self.mongod_data_folder = conf("mongod_data_folder", None)

        self.operating_system = self._build_operating_system_info(os_name)
        self.os_version = conf("os_version", os_ver)

        # For now order of the following line is important
        self.downloaded_version = None
        self.download_url = conf("download_url", self._build_download_url())

        self.url_hash = hashlib.sha256(bytes(self.download_url, "utf-8")).hexdigest()

        self.ignore_cache = conf("ignore_cache", ignore_cache, coerce_with=bool)
        self.use_local_mongod = conf("use_local_mongod", False, coerce_with=bool)

        self.download_folder = conf(
            "download_folder", mkdir_ifnot_exist(CACHE_FOLDER, "download")
        )
        self.extract_folder = conf(
            "extract_folder", mkdir_ifnot_exist(CACHE_FOLDER, "extract")
        )
        self.archive_folder = mkdir_ifnot_exist(self.download_folder, self.url_hash)
        self.extracted_folder = mkdir_ifnot_exist(self.extract_folder, self.url_hash)

    def __str__(self):
        return (
            f"Mongo Version {self.mongo_version}\n"
            f"MongoD Port {self.mongod_port}\n"
            f"MongoD Data Folder {self.mongod_data_folder}\n"
            f"OS Name {self.operating_system}\n"
            f"OS Version {self.os_version}\n"
            f"Download URL {self.download_url}\n"
            f"URL hash {self.url_hash}\n"
            f"Download Version {self.downloaded_version}\n"
            f"Ignore Cache {self.ignore_cache}\n"
            f"Use Local MongoD {self.use_local_mongod}\n"
            f"Download Folder {self.download_folder}\n"
            f"Extract Folder {self.extract_folder}\n"
        )

    def _build_operating_system_info(self, os_name=None):
        os_name = conf("operating_system", os_name)
        if os_name is None:
            _mapping = {"Darwin": "osx", "Linux": "linux", "Windows": "windows"}
            os_name = _mapping.get(platform.system())
            if os_name is None:
                raise OperatingSystemNotFound("Can't determine operating system.")
            else:
                if os_name == "linux":
                    logger.warning(
                        (
                            "Starting from MongoDB 4.0.23 "
                            "there isn't a generic Linux version of MongoDB"
                        )
                    )
        return os_name

    def _build_download_url(self):
        dl_url, downloaded_version = best_url(
            self.operating_system,
            version=self.mongo_version,
            os_ver=self.os_version,
        )

        self.downloaded_version = downloaded_version
        return dl_url
