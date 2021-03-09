from os import utime
import socket

from pymongo_inmemory import _utils


def test_find_open_port(monkeypatch):
    open_ports = (123, 125)

    class mock_socket():
        AF_INET = None
        SOCK_STREAM = None

        def __init__(self, *args, **kwargs):
            pass

        def connect_ex(self, obj):
            if obj[1] in open_ports:
                return 0
            return 42

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    monkeypatch.setattr(socket, "socket", mock_socket)
    assert _utils.find_open_port([123, 124]) == 124
    assert _utils.find_open_port([122, 123]) == 122
    assert _utils.find_open_port([123, 125, 122]) == 122


def test_environment_var_option(monkeypatch):
    monkeypatch.setenv("PYMONGOIM__SOME_VALUE", "42")
    assert _utils.conf("some_value") == "42"
    assert _utils.conf("SOME_VALUE") == "42"
    assert _utils.conf("SOME_OTHER_VALUE") is None


def test_make_semver():
    expected = _utils.make_semver("1.2.3")
    assert expected == _utils.SemVer(1, 2, 3)
    assert expected.major == 1
    assert expected.minor == 2
    assert expected.patch == 3
