import socket
from typing import Sequence


def find_open_port(sq: Sequence[int]) -> int:
    for port in sq:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            if 0 != soc.connect_ex(("localhost", port)):
                return port


def _sanitize_mongoclient_args(args, kwargs):
    if len(args) > 0 and str(args[0]).startswith("mongodb"):
        args = args[1:]
    for kw in ["host", "port"]:
        kwargs.pop(kw, None)
    return args, kwargs


if __name__ == "__main__":
    print(find_open_port([9001, 9002]))
