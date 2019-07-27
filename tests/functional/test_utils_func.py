import socket

from pymongo_inmemory import _utils


def test_find_open_port2():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setblocking(0)
        server.bind(("localhost", 12323))
        server.listen(5)

        assert _utils.find_open_port([12323, 12324]) == 12324
