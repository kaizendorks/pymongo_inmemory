"""Downloader module downloads appropriate version of mongo server TAR file.
The TAR file to download comes from MongoDB Communiti Edition doownload page:
    https://www.mongodb.com/download-center/community

However, it's not dynamically queried for now. Instead we have a predefined
patterns for download URLs.

Currently Windows is ignored.

Definition of operating system
Definition of version

Environmental variables > setup.cfg > automatic detection. If it's not possible
to determine, an error is thrown.
"""

import glob
import logging
import os
import platform
import stat
import shutil
import tarfile
import tempfile
import urllib.request as request

from ._utils import conf


DOWNLOAD_URL_PATTERNS = {
    "Darwin": "https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-{ver}.tgz"
}
FILE_NAME_PATTERN = "mongodb_archive_{ver}.tgz"
VERSIONS = {
    "Darwin": [
        "4.0.10",
        "3.6.13",
        "3.4.21",
        "3.2.22",
        "3.0.15",
    ]
}
CACHE_FOLDER = os.path.join(os.path.dirname(__file__), ".cache")
logger = logging.getLogger("PYMONGOIM_DOWNLOADER")


def _mkdir_ifnot_exist(folder_name):
    if not os.path.isdir(CACHE_FOLDER):
        os.mkdir(CACHE_FOLDER)
    path = os.path.join(CACHE_FOLDER, folder_name)
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


def _download_folder():
    return os.environ.get("PYMONGOIM__DOWNLOAD_FOLDER", _mkdir_ifnot_exist("download"))


def _extract_folder():
    return os.environ.get("PYMONGOIM__EXTRACT_FOLDER", _mkdir_ifnot_exist("extract"))


def bin_folder():
    return os.environ.get("PYMONGOIM__BIN_FOLDER", _mkdir_ifnot_exist("bin"))


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


def _download_tar(dl_url, tar_file, dst_file):
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
        request.urlretrieve(dl_url, filename=temp.name, reporthook=_dl_reporter)
        logger.debug("Finished download.")
        shutil.copyfile(temp.name, dst_file)
        logger.debug("Copied file to {}".format(dst_file))


def _extract(tar_file):
    extract_folder = _extract_folder()
    with tarfile.open(tar_file, "r") as t:
        logger.info("Starting extraction.")
        for f in t.getnames():
            logger.debug("Extracting {} to {}".format(f, extract_folder))
            t.extract(f, extract_folder)
            logger.debug("Done extracting {}".format(f))
        logger.info("Extractiong finished.")


def download(opsys=None, version=None):
    if version is None:
        version = str(conf("mongo_version"))
    if opsys is None:
        opsys = str(conf("operating_system"))

    dl_url = DOWNLOAD_URL_PATTERNS[platform.system()].format(ver=version)
    dl_folder = _download_folder()
    tar_file = os.path.join(dl_folder, FILE_NAME_PATTERN.format(ver=version))
    dst_file = os.path.join(dl_folder, FILE_NAME_PATTERN.format(ver=version))

    _mkdir_ifnot_exist("data")

    if os.path.isfile(os.path.join(bin_folder(), "mongod")):
        return
    if not os.path.isfile(tar_file):
        logger.info("Archive file is not found, {}".format(tar_file))
        _download_tar(dl_url, tar_file, dst_file)
        _extract(tar_file)
        _copy_bins()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    download()
