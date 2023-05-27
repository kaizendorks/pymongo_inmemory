from pymongo_inmemory.downloader import context


def test_environment_var_option(monkeypatch):
    monkeypatch.setenv("PYMONGOIM__SOME_VALUE", "42")
    assert context.conf("some_value") == "42"
    assert context.conf("SOME_VALUE") == "42"
    assert context.conf("SOME_OTHER_VALUE") is None
