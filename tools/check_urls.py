import argparse
from concurrent import futures
import hashlib
from http.client import HTTPSConnection
import logging
import time
from typing import List, Set
from random import randint

import click
from click._termui_impl import ProgressBar

from pymongo_inmemory.downloader._urls import URLS, expand_url_tree, ExpandedURL


logger = logging.getLogger("PYMONGOIM_URL_CHECKER")


def split(url):
    # Quick and dirty way to split host from rest, but it would work for our case
    parts = url.split("/")
    host = format(parts[2])
    rest = "/".join([""] + parts[3:])
    return host, rest


def check_url(expanded: ExpandedURL, progress_bar: ProgressBar):
    host, rest = split(expanded.url)

    # sleep some random time to prevent server side throttling
    time.sleep(randint(1, 4))

    progress_bar.update(1)

    conn = HTTPSConnection(host)
    conn.request("HEAD", rest)
    response = conn.getresponse()

    if response.status == 200:
        logger.debug(
            "SUCCESS: URL check for {} {} MongoDB {}".format(
                expanded.os_name,
                expanded.os_version,
                expanded.version,
            )
        )
    else:
        logger.debug(
            ("FAIL: URL check for {} {} " "MongoDB {}, {}, reason: {} {}").format(
                expanded.os_name,
                expanded.os_version,
                expanded.version,
                expanded.url,
                response.status,
                response.reason,
            )
        )
        return expanded


def check_hash(expanded: ExpandedURL, progress_bar: ProgressBar, hashes: Set[str]):
    progress_bar.update(1)

    _, rest = split(expanded.url)

    h = hashlib.sha256(bytes(rest, "utf8")).hexdigest()

    if h in hashes:
        logger.debug(
            "FAIL: Hash hit {} {} MongoDB {}, reason: filename {} with hash {}".format(
                expanded.os_name, expanded.os_version, expanded.version, rest, h
            )
        )
        return expanded
    else:
        hashes.add(h)
        logger.debug(
            ("SUCCESS: Hash for {} {} " "MongoDB {}, filename {} hash {}").format(
                expanded.os_name, expanded.os_version, expanded.version, rest, h
            )
        )


def failed_url_check(x: futures.Future):
    return x.result() is not None and x.exception() is not None


def execute_url_check(expanded_items, progress_bar: ProgressBar) -> List[ExpandedURL]:
    failed: List[ExpandedURL]
    with futures.ThreadPoolExecutor() as executor:
        for expanded in expanded_items:
            promises.append(executor.submit(check_url, expanded, progress_bar))

        futures.wait(promises)

        failed = [x.result() for x in promises if failed_url_check(x)]
    return failed


def execute_hash_check(expanded_items, progress_bar: ProgressBar) -> List[ExpandedURL]:
    failed: List[ExpandedURL] = []
    hashes: Set[str] = set()

    for expanded in expanded_items:
        checked = check_hash(expanded, progress_bar, hashes)
        if checked is not None:
            failed.append(expanded)

    return failed


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    arg_parser = argparse.ArgumentParser(prog="URL Checker")
    arg_parser.add_argument("--hashes", action="store_true")

    args = arg_parser.parse_args()

    promises = []
    failed = []

    logger.debug("Expanding URL tree")
    expanded_items = list(expand_url_tree(URLS))
    progress_bar_label = (
        "Checking uniqueness of versions"
        if args.hashes
        else "Checking downloadable packages"
    )

    logging.info("Starting checks.")
    with click.progressbar(
        length=len(expanded_items),
        label=progress_bar_label,
        fill_char="=",
        empty_char=" ",
        info_sep=" ",
        width=42,
        show_eta=False,
    ) as bar:
        if args.hashes:
            failed = execute_hash_check(expanded_items, bar)
        else:
            failed = execute_url_check(expanded_items, bar)

    logging.info("All checks done.")

    logging.warning("==== FAILED CHECKS ====")
    for x in failed:
        x: ExpandedURL = x
        logging.warning(
            " ".join(
                [
                    x.os_name,
                    x.os_version,
                    x.version,
                    x.url,
                ]
            )
        )
    logging.warning("==== / FAILED CHECKS ====")
