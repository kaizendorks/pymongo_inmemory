import os.path as path

import pytest

from pymongo_inmemory import downloader


def test_env_folders_overwrite_default_downloadfolder(monkeypatch):
    monkeypatch.setenv("PYMONGOIM__DOWNLOAD_FOLDER", "test_folder")
    assert downloader._download_folder() == "test_folder"


def test_env_folders_overwrite_default_extractfolder(monkeypatch):
    monkeypatch.setenv("PYMONGOIM__EXTRACT_FOLDER", "test_folder")
    assert downloader._extract_folder() == "test_folder"


def test_default_dl_folder(monkeypatch, tmpdir):
    monkeypatch.setattr(downloader, "CACHE_FOLDER", tmpdir)
    assert path.samefile(
        downloader._download_folder(),
        path.join(tmpdir, "download")
    )
    assert path.exists(path.join(tmpdir, "download"))


def test_default_extract_folder(monkeypatch, tmpdir):
    monkeypatch.setattr(downloader, "CACHE_FOLDER", tmpdir)
    assert path.samefile(
        downloader._extract_folder(),
        path.join(tmpdir, "extract")
    )
    assert path.exists(path.join(tmpdir, "extract"))


def test_extracted_folder(monkeypatch, tmpdir):
    monkeypatch.setattr(downloader, "CACHE_FOLDER", tmpdir)
    assert path.samefile(
        downloader._extracted_folder("mongodb-amazon2-x86_64-1.1.1.tar"),
        path.join(tmpdir, "extract", "mongodb-amazon2-x86_64-1.1.1-tar")
    )
    assert path.samefile(
        downloader._extracted_folder("mongodb-windows-x86_64-1.1.1.zip"),
        path.join(tmpdir, "extract", "mongodb-windows-x86_64-1.1.1-zip")
    )


def test_make_folder(monkeypatch, tmpdir):
    assert path.samefile(
        downloader._mkdir_ifnot_exist(tmpdir, "test"),
        path.join(tmpdir, "test")
    )
    assert path.exists(path.join(tmpdir, "test"))
    assert path.samefile(
        downloader._mkdir_ifnot_exist(tmpdir, "test2", "nested"),
        path.join(tmpdir, "test2", "nested")
    )
    assert path.exists(path.join(tmpdir, "test2", "nested"))


def test_fails_if_os_unknown(monkeypatch):
    def system():
        return "Unknown"

    def conf(*args, **kwargs):
        return
    monkeypatch.setattr(downloader.platform, "system", system)
    monkeypatch.setattr(downloader, "conf", conf)
    with pytest.raises(downloader.OperatingSystemNotFound):
        downloader.download()
