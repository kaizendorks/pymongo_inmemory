import socket

import pytest

from pymongo_inmemory import _utils


@pytest.fixture
def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setblocking(0)
        server.bind(("localhost", 12323))
        server.listen(5)
        yield server


def test_find_open_port(server):
    assert _utils.find_open_port([12323, 12324]) == 12324
