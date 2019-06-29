# -*- coding: utf8 -*-
import logging
import os
import platform
import shutil
import tempfile
import urllib.request as request


DOWNLOAD_URL_PATTERNS = {
    'Darwin': 'https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-{version}.tgz'
}
VERSIONS = {
    'Darwin': [
        '4.0.10',
        '3.6.13',
        '3.4.21',
        '3.2.22',
        '3.0.15',
    ]
}


def _download_folder() -> str:
    current_folder = os.path.dirname(__file__)
    default_download_folder = os.path.join(current_folder, '..', 'download')
    return os.environ.get('PYMONGOIM__DOWNLOAD_FOLDER', default_download_folder)


def _dl_reporter(blocknum, block_size, total_size):
    logger = logging.getLogger('PYMONGOIM_DOWNLOAD')
    percent_dled = blocknum * block_size / total_size * 100
    size_dlded = blocknum * block_size / 1024 / 1024  # MBs
    total_size = total_size / 1024 / 1024  # MBs
    logger.info('{:.0f} % ({:.0f} MiB of {:.0f} MiB)'.format(percent_dled, size_dlded, total_size))


def download(version: str):
    logger = logging.getLogger('PYMONGOIM_DOWNLOAD')
    dl_folder = _download_folder()
    dl_url = DOWNLOAD_URL_PATTERNS[platform.system()].format(version=version)
    if not os.path.isdir(dl_folder):
        logger.debug("Download folder doesn't exist, creating it.")
        os.mkdir(dl_folder)
    dst_file = os.path.join(dl_folder, 'mongodb_archive_{}.tgz'.format(version))
    if os.path.isfile(dst_file):
        logger.debug("There is already a downloaded file {}, skipping download".format(dst_file))
        return
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        logger.debug("Starting download to temporary location {}".format(temp.name))
        request.urlretrieve(dl_url, filename=temp.name, reporthook=_dl_reporter)
        logger.debug("Finished download.")
        shutil.copyfile(temp.name, dst_file)
        logger.debug("Copied file to {}".format(dst_file))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    download('4.0.10')
