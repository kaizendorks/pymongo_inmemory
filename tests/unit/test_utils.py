import os
import socket

from pymongo_inmemory import _utils
from pymongo_inmemory.mongod import _last_line


def test__last_line():
    assert _last_line(bytes(os.linesep, "utf8").join([b"Sometext", b"1234"])) == 1234
    assert (
        _last_line(bytes(os.linesep, "utf8").join([b"Sometext", b"1234"]), as_a=str)
        == "1234"
    )


def test_find_open_port(monkeypatch):
    open_ports = (123, 125)

    class mock_socket:
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


def test_make_semver():
    expected = _utils.make_semver("1.2.3")
    assert expected == _utils.SemVer(1, 2, 3)
    assert expected.major == 1
    assert expected.minor == 2
    assert expected.patch == 3

    expected = _utils.make_semver("4")
    assert expected == _utils.SemVer(4, None, None)
    assert expected.major == 4
    assert expected.minor is None
    assert expected.patch is None

    expected = _utils.make_semver("4.1")
    assert expected == _utils.SemVer(4, 1, None)
    assert expected.major == 4
    assert expected.minor == 1
    assert expected.patch is None

    expected = _utils.make_semver()
    assert expected == _utils.SemVer(None, None, None)
    assert expected.major is None
    assert expected.minor is None
    assert expected.patch is None
