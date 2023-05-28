import logging

from . import download
from ..context import Context


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    context = Context()
    download(context)
