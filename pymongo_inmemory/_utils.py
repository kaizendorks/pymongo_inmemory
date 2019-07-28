from configparser import ConfigParser
import socket


def find_open_port(sq):
    for port in sq:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            if 0 != soc.connect_ex(("localhost", port)):
                return port


DEFAULT_CONF = {
    "mongo_version": "4.0.10"
}


def conf(option):
    parser = ConfigParser()
    parser.read("setup.cfg")
    return parser.get(
        "pymongo_inmemory",
        option,
        fallback=DEFAULT_CONF.get(option, None),
        raw=True
    )


if __name__ == "__main__":
    # print(find_open_port([9001, 9002]))
    # print(conf("mongo_version"))
    pass
