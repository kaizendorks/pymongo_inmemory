# -*- coding: utf8 -*-
import glob
import logging
import os
import platform
import shutil
import tarfile
import tempfile
import urllib.request as request


DOWNLOAD_URL_PATTERNS = {
    "Darwin": "https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-{version}.tgz"
}
FILE_NAME_PATTERN = "mongodb_archive_{}.tgz"
VERSIONS = {
    "Darwin": [
        "4.0.10",
        "3.6.13",
        "3.4.21",
        "3.2.22",
        "3.0.15",
    ]
}
CACHE_FOLDER = os.path.join(os.path.dirname(__file__), "..", ".cache")


def _mkdir_ifnot_exist(folder_name: str) -> str:
    if not os.path.isdir(CACHE_FOLDER):
        os.mkdir(CACHE_FOLDER)
    path = os.path.join(CACHE_FOLDER, folder_name)
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


def _download_folder() -> str:
    return os.environ.get("PYMONGOIM__DOWNLOAD_FOLDER", _mkdir_ifnot_exist("download"))


def _extract_folder() -> str:
    return os.environ.get("PYMONGOIM__EXTRACT_FOLDER", _mkdir_ifnot_exist("extract"))


def bin_folder() -> str:
    return os.environ.get("PYMONGOIM__BIN_FOLDER", _mkdir_ifnot_exist("bin"))


def _dl_reporter(blocknum, block_size, total_size):
    logger = logging.getLogger("PYMONGOIM_DOWNLOAD")
    percent_dled = blocknum * block_size / total_size * 100
    size_dlded = blocknum * block_size / 1024 / 1024  # MBs
    total_size = total_size / 1024 / 1024  # MBs
    logger.info("{:.0f} % ({:.0f} MiB of {:.0f} MiB)".format(
        percent_dled, size_dlded, total_size)
    )


def _copy_bins():
    logger = logging.getLogger("PYMONGOIM_COPYBINS")
    extract_folder = _extract_folder()
    bin_path = bin_folder()
    for binfile_path in glob.iglob(
        os.path.join(extract_folder, "**/bin/*"), recursive=True
    ):
        binfile_name = os.path.basename(binfile_path)
        logger.debug("Copying {} to bin folder".format(binfile_name))
        shutil.copyfile(
            binfile_path, os.path.join(bin_path, binfile_name)
        )
        logger.debug("Copied {}".format(binfile_name))


def _download_tar(version: str):
    logger = logging.getLogger("PYMONGOIM_DOWNLOAD")
    dl_folder = _download_folder()
    dl_url = DOWNLOAD_URL_PATTERNS[platform.system()].format(version=version)
    if not os.path.isdir(dl_folder):
        logger.debug("Download folder doesn't exist, creating it.")
        os.mkdir(dl_folder)
    dst_file = os.path.join(dl_folder, FILE_NAME_PATTERN.format(version))
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


def _extract(version: str):
    logger = logging.getLogger("PYMONGOIM_EXTRACT")
    tar_file = os.path.join(_download_folder(), FILE_NAME_PATTERN.format(version))
    if not os.path.isfile(tar_file):
        logger.error("Archive file is not found, {}".format(tar_file))
        _download_tar(version)
    extract_folder = _extract_folder()
    with tarfile.open(tar_file, "r") as t:
        logger.info("Starting extraction.")
        for f in t.getnames():
            logger.debug("Extracting {} to {}".format(f, extract_folder))
            t.extract(f, extract_folder)
            logger.debug("Done extracting {}".format(f))
        logger.info("Extractiong finished.")


def download(version: str = "4.0.10"):  # TODO: Get version automatically
    _extract(version)
    _copy_bins()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    download()
