from http.client import HTTPSConnection
import logging

from ._urls import URLS, expand_url_tree


logger = logging.getLogger("PYMONGOIM_URL_CHECKER")


def split(url):
    # Quick and dirty way to split host from rest, but it would work for our case
    parts = url.split("/")
    host = format(parts[2])
    rest = "/".join([""] + parts[3:])
    return host, rest


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    for expanded in expand_url_tree(URLS):
        logger.debug("Checking URL for {} {} MongoDB {}".format(
            expanded.os_name,
            expanded.os_version,
            expanded.version,
        ))
        host, rest = split(expanded.url)

        conn = HTTPSConnection(host)
        conn.request("HEAD", rest)
        response = conn.getresponse()

        if response.status == 200:
            logger.debug("Success")
        else:
            logger.error((
                "URL check failed for {} {} "
                "MongoDB {}, {}, reason: {} {}"
            ).format(
                expanded.os_name,
                expanded.os_version,
                expanded.version,
                expanded.url,
                response.status,
                response.reason
            ))
