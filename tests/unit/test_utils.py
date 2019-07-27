import socket

from pymongo_inmemory import _utils


def test_sanitize_mongoclient_args_removes_right_args():
    args = (
        "mongodb://somepath",
        "27017",
    )
    expected_args = (
        "27017",
    )
    actual_args, _ = _utils._sanitize_mongoclient_args(args, {})
    assert actual_args == expected_args


def test_sanitize_mongoclient_args_works_with_empty_args():
    actual_args, _ = _utils._sanitize_mongoclient_args((), {})
    assert actual_args == ()


def test_sanitize_mongoclient_args_removes_right_kwargs():
    kwargs = {
        "host": "myhost",
        "port": 27017,
        "document_class": dict
    }
    expected_kwargs = {
        "document_class": dict
    }
    _, actual_kwargs = _utils._sanitize_mongoclient_args((), kwargs)
    assert actual_kwargs == expected_kwargs


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
