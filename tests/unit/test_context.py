from pymongo_inmemory import context

import pytest


def test_environment_var_option(monkeypatch):
    monkeypatch.setenv("PYMONGOIM__SOME_VALUE", "42")
    assert context.conf("some_value") == "42"
    assert context.conf("SOME_VALUE") == "42"
    assert context.conf("SOME_OTHER_VALUE") is None


def test_env_folders_overwrite_default_downloadfolder(monkeypatch):
    monkeypatch.setenv("PYMONGOIM__DOWNLOAD_FOLDER", "test_folder")
    pim_context = context.Context()
    assert pim_context.download_folder == "test_folder"


def test_env_folders_overwrite_default_extractfolder(monkeypatch):
    monkeypatch.setenv("PYMONGOIM__EXTRACT_FOLDER", "test_folder")
    pim_context = context.Context()
    assert pim_context.extract_folder == "test_folder"


def test_fails_if_os_unknown(monkeypatch):
    def system():
        return "Unknown"

    def conf(*args, **kwargs):
        return

    monkeypatch.setattr(context.platform, "system", system)
    monkeypatch.setattr(context, "conf", conf)
    with pytest.raises(context.OperatingSystemNotFound):
        context.Context()
