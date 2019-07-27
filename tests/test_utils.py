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
