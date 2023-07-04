import os
import shutil
import tarfile
import urllib.request as request

import pytest

from pymongo_inmemory import downloader
from pymongo_inmemory import context


@pytest.fixture
def make_mongo_payload():
    def _make_payload(_path):
        mongod_path = _path / "mongod"
        tar_path = _path / "mongodb-macos-x86_64-4.0.1.tar"

        # Create a dummy text file and archive it.
        with open(mongod_path, "a") as f:
            f.write("Something")
        with tarfile.open(tar_path, mode="w") as t:
            t.addfile(
                tarfile.TarInfo("mongodb-macos-x86_64-4.0.1/bin/mongod"), mongod_path
            )

    return _make_payload


@pytest.fixture
def urlretrieve_patcher():
    def patcher(tarpath):
        """Fixture returns this so that test can create a patch with `_path`"""

        def _urlretrieve_patch(*args, **kwargs):
            filename = kwargs.get("filename")
            if filename is None:
                raise AssertionError("kwarg `filename` has to be provided.")
            shutil.copyfile(tarpath, filename)

        return _urlretrieve_patch

    return patcher


def test_downloader(make_mongo_payload, urlretrieve_patcher, monkeypatch, tmpdir):
    make_mongo_payload(tmpdir)
    monkeypatch.setattr(context, "CACHE_FOLDER", tmpdir / ".cache")

    urlretrieve = urlretrieve_patcher(tmpdir / "mongodb-macos-x86_64-4.0.1.tar")
    monkeypatch.setattr(request, "urlretrieve", urlretrieve)

    pim_context = context.Context(os_name="osx", version="4.0.1", os_ver="generic")

    bin_dir = downloader.download(pim_context)
    expected_mongod_path = os.path.join(bin_dir, "mongod")
    assert os.path.isfile(expected_mongod_path)
