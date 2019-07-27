import os.path as path

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


def test_can_get_default_bin_folder():
    assert path.samefile(
        downloader.bin_folder(),
        path.join(
            path.dirname(__file__),
            "..", "..",
            "pymongo_inmemory", ".cache", "bin"
        )
    )
