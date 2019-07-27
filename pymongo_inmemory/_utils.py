import socket
from typing import Sequence


def find_open_port(sq: Sequence[int]) -> int:
    for port in sq:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            if 0 != soc.connect_ex(("localhost", port)):
                return port


if __name__ == "__main__":
    print(find_open_port([9001, 9002]))
