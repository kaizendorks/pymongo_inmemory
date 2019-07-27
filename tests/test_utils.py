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
