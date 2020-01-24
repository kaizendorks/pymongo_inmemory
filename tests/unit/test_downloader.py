import os.path as path

import pytest

from pymongo_inmemory import downloader


def test_env_folders_overwrite_default_downloadfolder(monkeypatch):
    monkeypatch.setenv("PYMONGOIM__DOWNLOAD_FOLDER", "test_folder")
    assert downloader._download_folder() == "test_folder"


def test_env_folders_overwrite_default_extractfolder(monkeypatch):
    monkeypatch.setenv("PYMONGOIM__EXTRACT_FOLDER", "test_folder")
    assert downloader._extract_folder() == "test_folder"


def test_env_folders_overwrite_default_binfolder(monkeypatch):
    monkeypatch.setenv("PYMONGOIM__BIN_FOLDER", "test_folder")
    assert downloader.bin_folder() == "test_folder"


def test_default_bin_folder(monkeypatch, tmpdir):
    monkeypatch.setattr(downloader, "CACHE_FOLDER", tmpdir)
    assert path.samefile(
        downloader.bin_folder(),
        path.join(tmpdir, "bin")
    )


def test_default_dl_folder(monkeypatch, tmpdir):
    monkeypatch.setattr(downloader, "CACHE_FOLDER", tmpdir)
    assert path.samefile(
        downloader._download_folder(),
        path.join(tmpdir, "download")
    )


def test_default_extract_folder(monkeypatch, tmpdir):
    monkeypatch.setattr(downloader, "CACHE_FOLDER", tmpdir)
    assert path.samefile(
        downloader._extract_folder(),
        path.join(tmpdir, "extract")
    )


def test_make_folder(monkeypatch, tmpdir):
    monkeypatch.setattr(downloader, "CACHE_FOLDER", tmpdir)
    assert path.samefile(
        downloader._mkdir_ifnot_exist("test"),
        path.join(tmpdir, "test")
    )


def test_fails_if_os_unknown(monkeypatch):
    def system():
        return "Unknown"
    def conf(*args, **kwargs):
        return
    monkeypatch.setattr(downloader.platform, "system", system)
    monkeypatch.setattr(downloader, "conf", conf)
    with pytest.raises(downloader.OperatingSystemNotFound):
        downloader.download()
