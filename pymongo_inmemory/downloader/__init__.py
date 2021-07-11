import glob
import zipfile
import logging
import os
from os import path
import platform
import shutil
import tarfile
import tempfile
import urllib.request as request
from urllib.error import HTTPError

from .._utils import conf
from ._urls import best_url


CACHE_FOLDER = path.join(path.dirname(__file__), "..", ".cache")

logger = logging.getLogger("PYMONGOIM_DOWNLOADER")


class OperatingSystemNotFound(ValueError):
    pass


class CantDownload(Exception):
    pass


class InvalidDownloadedFile(Exception):
    pass


def _mkdir_ifnot_exist(*folders):
    current_path = path.join(folders[0])
    if not path.isdir(current_path):
        os.mkdir(current_path)
    for x in folders[1:]:
        current_path = path.join(current_path, x)
        if not path.isdir(current_path):
            os.mkdir(current_path)
    return current_path


def _download_folder():
    return conf("download_folder", _mkdir_ifnot_exist(CACHE_FOLDER, "download"))


def _extract_folder():
    return conf("extract_folder", _mkdir_ifnot_exist(CACHE_FOLDER, "extract"))


def _extracted_folder(archive_file):
    "Defines a nested versioned folder in the extract base folder"
    base_folder = _extract_folder()
    base_name = path.basename(archive_file).split(".")
    file_name = ".".join(base_name[:-1])
    extension = base_name[-1]
    archive_folder = "-".join([file_name, extension])
    return _mkdir_ifnot_exist(base_folder, archive_folder)


def _dl_reporter(blocknum, block_size, total_size):
    percent_dled = blocknum * block_size / total_size * 100
    size_dlded = blocknum * block_size / 1024 / 1024  # MBs
    total_size = total_size / 1024 / 1024  # MBs
    if 0 <= percent_dled % 10 <= 0.01:
        logger.info("{:.0f} % ({:.0f} MiB of {:.0f} MiB)".format(
            percent_dled, size_dlded, total_size)
        )


def _download_file(dl_url, destination_file):
    dl_folder = _download_folder()

    if not path.isdir(dl_folder):
        logger.debug("Download folder doesn't exist, creating it.")
        os.mkdir(dl_folder)

    if path.isfile(destination_file):
        logger.debug((
            "There is already a downloaded file {}, "
            "skipping download"
        ).format(destination_file))
        return

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        logger.debug("Starting download to temporary location {}".format(temp.name))
        try:
            request.urlretrieve(dl_url, filename=temp.name, reporthook=_dl_reporter)
        except HTTPError:
            raise CantDownload((
                "Can't download {url}, "
                "make sure MongoDB provides it. "
                "Possibly the version is not provided for the operating system."
            ).format(url=dl_url))

        logger.debug("Finished download.")
        shutil.copyfile(temp.name, destination_file)
        logger.debug("Copied file to {}".format(destination_file))


def _extract(archive_file):
    logger.info("Extracting from the archive, {}".format(archive_file))
    extract_folder = _extracted_folder(archive_file)

    if tarfile.is_tarfile(archive_file):
        _extract_tar(archive_file, extract_folder)
    elif zipfile.is_zipfile(archive_file):
        _extract_zip(archive_file, extract_folder)
    else:
        raise InvalidDownloadedFile("Expecting either a .tar or a .zip file.")


def _extract_tar(tar_file, extract_folder):
    with tarfile.open(tar_file, "r") as t:
        logger.info("Starting extraction.")
        for f in t.getnames():
            logger.debug("Extracting {} to {}".format(f, extract_folder))
            t.extract(f, extract_folder)
            logger.debug("Done extracting {}".format(f))
        logger.info("Extractiong finished.")


def _extract_zip(zip_file, extract_folder):
    with zipfile.ZipFile(zip_file) as z:
        logger.info("Starting extraction.")
        for f in z.namelist():
            logger.debug("Extracting {} to {}".format(f, extract_folder))
            z.extract(f, extract_folder)
            logger.debug("Done extracting {}".format(f))
        logger.info("Extractiong finished.")


def _collect_archive_name(url):
    return url.split("/")[-1]


def _get_mongod(base):
    for binfile_path in glob.iglob(
        path.join(base, "**/bin/*"), recursive=True
    ):
        binfile_name = path.basename(binfile_path)
        try:
            binfile_name.index("mongod")
        except ValueError:
            continue
        else:
            return binfile_path


def _has_mongod(extracted_folder):
    return _get_mongod(extracted_folder) is not None


def download(os_name=None, version=None, os_ver=None, ignore_cache=False):
    """Download MongoDB binaries.
    Available versions are collected form this URL:
    https://www.mongodb.com/download-center/community/releases
    and this one:
    https://www.mongodb.com/download-center/community/releases/archive

    Parameters
    ----------
    os_name: str
        If `None`, then it'll try to determine based on `platform.system()`, if can't
        determined `OperatingSystemNotFound` will be raised
    version: str
        MongoDB version
    os_ver: str
        Operating system version, if the OS has several versions
    ignore_cache: bool
        Download MongoDB, even if there is already one in the cache

    Raises
    ------
    OperatingSystemNotFound: If OS is not MacOS, Windows or Linux variant.
    """
    if version is None:
        version = conf("mongo_version")

    if os_name is None:
        os_name = conf("operating_system")
        if os_name is None:
            _mapping = {"Darwin": "osx", "Linux": "linux", "Windows": "windows"}
            os_name = _mapping.get(platform.system())
            if os_name is None:
                raise OperatingSystemNotFound("Can't determine operating system.")

    if os_name == "linux":
        logger.warn((
            "Starting from MongoDB 4.0.23 "
            "there isn't a generic Linux version of MongoDB"
            ))

    if os_ver is None:
        os_ver = conf("os_version")

    dl_url = conf("download_url", best_url(
        os_name,
        version=version,
        os_ver=os_ver
    ))

    logger.debug("Downloading MongoD from {}".format(dl_url))
    dl_folder = _download_folder()
    archive_file = path.join(dl_folder, _collect_archive_name(dl_url))

    should_ignore_cache = bool(conf("ignore_cache", ignore_cache))

    if should_ignore_cache or not path.isfile(archive_file):
        logger.info("Archive file is not found, {}".format(archive_file))
        _download_file(dl_url, archive_file)
        _extract(archive_file)

    extracted_dir = _extracted_folder(archive_file)
    if not _has_mongod(extracted_dir):
        _extract(archive_file)

    return path.dirname(_get_mongod(extracted_dir))
