"""Downloader module downloads appropriate version of mongo server TAR file.
The TAR file to download comes from MongoDB Communiti Edition doownload page:
    https://www.mongodb.com/download-center/community

However, it's not dynamically queried for now. Instead we have a predefined
patterns for download URLs.

Currently Windows is ignored.

Operating systems can be one of these:
    osx
    linux
    amazonlinux
    amazonlinux2
    debian7
    debian8
    debian9
    rhel5
    rhel6
    rhel7
    suse11
    suse12
    ubuntu14
    ubuntu16
    ubuntu18
    windows
If OS can't be determined an exception is thrown.

Versions should be one of these, but not all versions are available for any
operating system, so it might not be downloaded:
    4.0
    3.6
    3.4
    3.2
    3.0
"""

import glob
import zipfile
import logging
import os
import platform
import stat
import shutil
import tarfile
import tempfile
import urllib.request as request
from urllib.error import HTTPError

from .._utils import conf
from ._url_tools import best_url


TARFILE_PATTERN = "mongodb_archive_{ver}.tgz"
ZIPFILE_PATTERN = "mongodb_archive_{ver}.zip"
CACHE_FOLDER = os.path.join(os.path.dirname(__file__), "..", ".cache")

logger = logging.getLogger("PYMONGOIM_DOWNLOADER")


class OperatingSystemNotFound(ValueError):
    pass


class CantDownload(Exception):
    pass


class InvalidDownloadedFile(Exception):
    pass


def _mkdir_ifnot_exist(folder_name):
    if not os.path.isdir(CACHE_FOLDER):
        os.mkdir(CACHE_FOLDER)
    path = os.path.join(CACHE_FOLDER, folder_name)
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


def _download_folder():
    return conf("download_folder", _mkdir_ifnot_exist("download"))


def _extract_folder():
    return conf("extract_folder", _mkdir_ifnot_exist("extract"))


def bin_folder():
    return conf("bin_folder", _mkdir_ifnot_exist("bin"))


def _dl_reporter(blocknum, block_size, total_size):
    percent_dled = blocknum * block_size / total_size * 100
    size_dlded = blocknum * block_size / 1024 / 1024  # MBs
    total_size = total_size / 1024 / 1024  # MBs
    if 0 <= percent_dled % 10 <= 0.01:
        logger.info("{:.0f} % ({:.0f} MiB of {:.0f} MiB)".format(
            percent_dled, size_dlded, total_size)
        )


def _copy_bins():
    extract_folder = _extract_folder()
    bin_path = bin_folder()
    for binfile_path in glob.iglob(
        os.path.join(extract_folder, "**/bin/*"), recursive=True
    ):
        binfile_name = os.path.basename(binfile_path)
        logger.debug("Copying {} to bin folder".format(binfile_name))
        target = os.path.join(bin_path, binfile_name)
        shutil.copyfile(binfile_path, target)
        os.chmod(target, (
            stat.S_IRUSR
            | stat.S_IXUSR
            | stat.S_IRGRP
            | stat.S_IXGRP
            | stat.S_IROTH
            | stat.S_IXOTH
        ))
        logger.debug("Copied {}".format(binfile_name))


def _download_file(dl_url, dst_file):
    dl_folder = _download_folder()

    if not os.path.isdir(dl_folder):
        logger.debug("Download folder doesn't exist, creating it.")
        os.mkdir(dl_folder)

    if os.path.isfile(dst_file):
        logger.debug((
            "There is already a downloaded file {}, "
            "skipping download"
        ).format(dst_file))
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
        shutil.copyfile(temp.name, dst_file)
        logger.debug("Copied file to {}".format(dst_file))


def _extract(downloaded_file):
    extract_folder = _extract_folder()
    if tarfile.is_tarfile(downloaded_file):
        _extract_tar(downloaded_file, extract_folder)
    elif zipfile.is_zipfile(downloaded_file):
        _extract_zip(downloaded_file, extract_folder)
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


def download(os_name=None, version=None, os_ver=None):
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
        Not all versions are available for all operating systems.

    Raises
    ------
    OperatingSystemNotFound: If download pattern can't be determined.
    """
    if version is None:
        version = str(conf("mongo_version"))

    if os_name is None:
        os_name = conf("operating_system")
        if os_name is None:
            _mapping = {"Darwin": "osx", "Linux": "linux", "Windows": "windows"}
            os_name = _mapping.get(platform.system())
            if os_name is None:
                raise OperatingSystemNotFound("Can't determine operating system.")

    if os_name == "linux":
        logger.warn((
            "Starting from MongoDB 4.2 "
            "there isn't a generic Linux version of MongoDB"
            ))

    if os_ver is None:
        os_ver = conf("os_version")

    dl_url = conf("download_url", best_url(os_name, version, os_ver))
    downloaded_file_pattern = ZIPFILE_PATTERN if os_name == 'windows' else TARFILE_PATTERN  # noqa E501

    logger.debug("Downloading MongoD from {}".format(dl_url))
    dl_folder = _download_folder()
    downloaded_file = os.path.join(
        dl_folder,
        downloaded_file_pattern.format(ver=version)
    )
    dst_file = os.path.join(dl_folder, downloaded_file_pattern.format(ver=version))

    if (
        os.path.isfile(os.path.join(bin_folder(), "mongod")) or
        os.path.isfile(os.path.join(bin_folder(), "mongod.exe"))
    ):
        return

    should_ignore_cache = conf("ignore_cache", False)

    if should_ignore_cache or not os.path.isfile(downloaded_file):
        logger.info("Archive file is not found, {}".format(downloaded_file))
        _download_file(dl_url, dst_file)
    else:
        # There is a downloaded file and mongod is missing, reextract
        logger.info("Extracting from the archive, {}".format(downloaded_file))
    _extract(downloaded_file)
    _copy_bins()
