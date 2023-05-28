import glob
import zipfile
import logging
import os
from os import path
import shutil
import tarfile
import tempfile
import urllib.request as request
from urllib.error import HTTPError

from ..context import Context


CACHE_FOLDER = path.join(path.dirname(__file__), "..", ".cache")

logger = logging.getLogger("PYMONGOIM_DOWNLOADER")


class OperatingSystemNotFound(ValueError):
    pass


class CantDownload(Exception):
    pass


class InvalidDownloadedFile(Exception):
    pass


def _dl_reporter(blocknum, block_size, total_size):
    percent_dled = blocknum * block_size / total_size * 100
    size_dlded = blocknum * block_size / 1024 / 1024  # MBs
    total_size = total_size / 1024 / 1024  # MBs
    if 0 <= percent_dled % 10 <= 0.01:
        logger.info(
            "{:.0f} % ({:.0f} MiB of {:.0f} MiB)".format(
                percent_dled, size_dlded, total_size
            )
        )


def _download_file(dl_url, destination_file, dl_folder):
    if not path.isdir(dl_folder):
        logger.debug("Download folder doesn't exist, creating it.")
        os.mkdir(dl_folder)

    if path.isfile(destination_file):
        logger.debug(
            ("There is already a downloaded file {}, " "skipping download").format(
                destination_file
            )
        )
        return

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        logger.debug("Starting download to temporary location {}".format(temp.name))
        try:
            request.urlretrieve(dl_url, filename=temp.name, reporthook=_dl_reporter)
        except HTTPError:
            raise CantDownload(
                (
                    "Can't download {url}, "
                    "make sure MongoDB provides it. "
                    "Possibly the version is not provided for the operating system."
                ).format(url=dl_url)
            )

        logger.debug("Finished download.")
        shutil.copyfile(temp.name, destination_file)
        logger.debug("Copied file to {}".format(destination_file))


def _extract(archive_file, extract_folder):
    logger.info("Extracting from the archive, {}".format(archive_file))

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


def _get_mongod(version, extract_folder):
    for binfile_path in glob.iglob(
        path.join(extract_folder, f"**{version}**/bin/*"), recursive=True
    ):
        binfile_name = path.basename(binfile_path)
        try:
            binfile_name.index("mongod")
        except ValueError:
            continue
        else:
            return binfile_path


def download(pim_context: Context):
    """Download MongoDB binaries.
    Available versions are collected form this URL:
    https://www.mongodb.com/download-center/community/releases
    and this one:
    https://www.mongodb.com/download-center/community/releases/archive
    """
    dl_url = pim_context.download_url
    downloaded_version = pim_context.downloaded_version

    logger.debug("Downloading MongoD from {}".format(dl_url))
    archive_file = path.join(pim_context.download_folder, _collect_archive_name(dl_url))

    should_ignore_cache = pim_context.ignore_cache

    if should_ignore_cache or not path.isfile(archive_file):
        logger.info("Archive file is not found, {}".format(archive_file))
        _download_file(dl_url, archive_file, pim_context.download_folder)
        _extract(archive_file, pim_context.extract_folder)

    if _get_mongod(downloaded_version, pim_context.extract_folder) is None:
        _extract(archive_file, pim_context.extract_folder)

    return path.dirname(_get_mongod(downloaded_version, pim_context.extract_folder))
