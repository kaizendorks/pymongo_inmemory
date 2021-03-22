from concurrent import futures
from http.client import HTTPSConnection
import logging
import time
from random import randint

from ._urls import URLS, expand_url_tree, ExpandedURL


logger = logging.getLogger("PYMONGOIM_URL_CHECKER")


def split(url):
    # Quick and dirty way to split host from rest, but it would work for our case
    parts = url.split("/")
    host = format(parts[2])
    rest = "/".join([""] + parts[3:])
    return host, rest


def check_url(expanded: ExpandedURL):
    host, rest = split(expanded.url)

    # sleep some random time to prevent server side throttling
    time.sleep(randint(1, 4))

    conn = HTTPSConnection(host)
    conn.request("HEAD", rest)
    response = conn.getresponse()

    if response.status == 200:
        logger.debug("SUCCESS: URL check for {} {} MongoDB {}".format(
            expanded.os_name,
            expanded.os_version,
            expanded.version,
        ))
    else:
        logger.error((
            "FAIL: URL check for {} {} "
            "MongoDB {}, {}, reason: {} {}"
        ).format(
            expanded.os_name,
            expanded.os_version,
            expanded.version,
            expanded.url,
            response.status,
            response.reason
        ))
        return expanded


def failed_url_check(x: futures.Future):
    return x.result() is not None and x.exception() is not None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    promises = []
    failed = []
    logging.info("Starting checks.")
    with futures.ThreadPoolExecutor() as executor:
        for expanded in expand_url_tree(URLS):
            promises.append(executor.submit(check_url, expanded))

        futures.wait(promises)
        logging.info("All checks done.")

        failed = [x.result() for x in promises if failed_url_check(x)]

    print("= FAILED CHECKS ============================================================")
    for x in failed:
        print(
            expanded.os_name,
            expanded.os_version,
            expanded.version,
            expanded.url,
        )
    print("============================================================================")
