import pytest  # noqa: F401

from pymongo_in_memory import downloader


def test_env_folders_overwrite_default_downloadfolder(monkeypatch):
    monkeypatch.setenv('PYMONGOIM__DOWNLOAD_FOLDER', 'test_folder')
    assert downloader._download_folder() == 'test_folder'


def test_env_folders_overwrite_default_extractfolder(monkeypatch):
    monkeypatch.setenv('PYMONGOIM__EXTRACT_FOLDER', 'test_folder')
    assert downloader._extract_folder() == 'test_folder'


def test_env_folders_overwrite_default_binfolder(monkeypatch):
    monkeypatch.setenv('PYMONGOIM__BIN_FOLDER', 'test_folder')
    assert downloader._bin_folder() == 'test_folder'
