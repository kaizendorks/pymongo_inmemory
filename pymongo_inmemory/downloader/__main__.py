import logging

from . import download


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    download("ubuntu", os_ver="18")
