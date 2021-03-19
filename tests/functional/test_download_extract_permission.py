import os
import shutil
import stat
import sys
import tarfile
import urllib.request as request
import warnings

import pytest

from pymongo_inmemory import downloader


@pytest.fixture
def make_mongo_payload():
    def _make_payload(_path):
        mongod_path = _path / "mongod"
        tar_path = _path / "test_archive.tar"

        # Create a dummy text file and archive it.
        with open(mongod_path, "a") as f:
            f.write("Something")
        with tarfile.open(tar_path, mode="w") as t:
            t.addfile(tarfile.TarInfo("bin/mongod"), mongod_path)
    return _make_payload


@pytest.fixture
def urlretrieve_patcher():
    def patcher(tarpath):
        """Fixture returns this so that test can create a patch with `_path`
        """
        def _urlretrieve_patch(*args, **kwargs):
            filename = kwargs.get("filename")
            if filename is None:
                raise AssertionError("kwarg `filename` has to be provided.")
            shutil.copyfile(tarpath, filename)
        return _urlretrieve_patch
    return patcher


@pytest.fixture
def extracted_folder_patcher():
    def patcher():
        def _extracted_folder(*args, **kwargs):
            return downloader._extract_folder()
        return _extracted_folder
    return patcher


def test_downloader(
    make_mongo_payload,
    urlretrieve_patcher,
    extracted_folder_patcher,
    monkeypatch,
    tmpdir
):
    make_mongo_payload(tmpdir)
    monkeypatch.setattr(downloader, "CACHE_FOLDER", tmpdir / ".cache")

    monkeypatch.setattr(downloader, "_extracted_folder", extracted_folder_patcher())

    urlretrieve = urlretrieve_patcher(tmpdir / "test_archive.tar")
    monkeypatch.setattr(request, "urlretrieve", urlretrieve)

    downloader.download(os_name="osx", os_ver="generic", version="4.0.1")
    expected_mongod_path = tmpdir / ".cache" / "bin" / "mongod"
    assert os.path.isfile(expected_mongod_path)

    # chmod can only create read-only files on windows,
    # so this assertion fails even though code is doing its job
    if sys.platform.startswith("win"):
        warnings.warn("Skipping file permission assertion on Windows")
    else:
        st = os.stat(expected_mongod_path)
        assert stat.filemode(st.st_mode) == "-r-xr-xr-x"
