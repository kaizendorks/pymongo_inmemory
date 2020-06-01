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

from ._utils import conf


TARFILE_PATTERN = "mongodb_archive_{ver}.tgz"
ZIPFILE_PATTERN = "mongodb_archive_{ver}.zip"
CACHE_FOLDER = os.path.join(os.path.dirname(__file__), ".cache")
DOWNLOAD_URL_PATTERNS = {
    "osx": {
        "url": "https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-{ver}.tgz",
        "file_pattern": TARFILE_PATTERN,
    },
    "linux": {
        "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-{ver}.tgz",
        "file_pattern": TARFILE_PATTERN,
    },
    "amazonlinux": {
        "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon-{ver}.tgz",
        "file_pattern": TARFILE_PATTERN,
    },
    "amazonlinux2": {
        "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon2-{ver}.tgz",
        "file_pattern": TARFILE_PATTERN,
    },
    "debian7": {
        "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian71-{ver}.tgz",  # noqa E501
        "file_pattern": TARFILE_PATTERN,
    },
    "debian8": {
        "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian81-{ver}.tgz",  # noqa E501
        "file_pattern": TARFILE_PATTERN,
    },
    "debian9": {
        "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian92-{ver}.tgz",  # noqa E501
        "file_pattern": TARFILE_PATTERN,
    },
    "rhel5": {
        "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel55-{ver}.tgz",
        "file_pattern": TARFILE_PATTERN,
    },
    "rhel6": {
        "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel62-{ver}.tgz",
        "file_pattern": TARFILE_PATTERN,
    },
    "rhel7": {
        "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-{ver}.tgz",
        "file_pattern": TARFILE_PATTERN,
    },
    "suse11": {
        "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse11-{ver}.tgz",
        "file_pattern": TARFILE_PATTERN,
    },
    "suse12": {
        "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse12-{ver}.tgz",
        "file_pattern": TARFILE_PATTERN,
    },
    "ubuntu14": {
        "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1404-{ver}.tgz",  # noqa E501
        "file_pattern": TARFILE_PATTERN,
    },
    "ubuntu16": {
        "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1604-{ver}.tgz",  # noqa E501
        "file_pattern": TARFILE_PATTERN,
    },
    "ubuntu18": {
        "url": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-{ver}.tgz",  # noqa E501
        "file_pattern": TARFILE_PATTERN,
    },
    "windows": {
        "url": "https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-{ver}.zip",  # noqa E501
        "file_pattern": ZIPFILE_PATTERN,
    },
}
VERSIONS = {
    "4.0": "4.0.10",
    "3.6": "3.6.13",
    "3.4": "3.4.21",
    "3.2": "3.2.22",
    "3.0": "3.0.15",
}
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


def download(opsys=None, version=None):
    """Download MongoDB binaries.

    Parameters
    ----------
    opsys: str
        Operating system. Should be one of these: osx, linux, amazonlinux, amazonlinux2,
        debian7, debian8, debian9, rhel5, rhel6, rhel7, suse11, suse12, ubuntu14,
        ubuntu16, ubuntu18, windows
        If `None`, then it'll try to determine based on `paltform.system()`, if can't
        determined `OperatingSystemNotFound` will be raised
    version: str
        MongoDB version, should be one of these: 4.0, 3.6, 3.4, 3.2, 3.0
        Not all versions are available for all operating systems. Check this URL:
        https://www.mongodb.com/download-center/community

    Raises
    ------
    OperatingSystemNotFound: If download pattern can't be determined.
    """
    if version is None:
        version = str(conf("mongo_version"))
    if opsys is None:
        opsys = conf("operating_system")
        if opsys is None:
            _mapping = {"Darwin": "osx", "Linux": "linux", "Windows": "windows"}
            opsys = _mapping.get(platform.system())
            if opsys is None:
                raise OperatingSystemNotFound("Can't find operating system.")

    version = VERSIONS.get(version, "4.0.10")
    dl_pattern = DOWNLOAD_URL_PATTERNS.get(opsys)["url"]
    downloaded_file_pattern = DOWNLOAD_URL_PATTERNS.get(opsys)["file_pattern"]

    dl_url = dl_pattern.format(ver=version)
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

    if not os.path.isfile(downloaded_file):
        logger.info("Archive file is not found, {}".format(downloaded_file))
        _download_file(dl_url, dst_file)
    else:
        # There is a downloaded file and mongod is missing, reextract
        logger.info("Extracting from the archive, {}".format(downloaded_file))
    _extract(downloaded_file)
    _copy_bins()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    download()
