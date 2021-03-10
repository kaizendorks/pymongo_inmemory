from collections import namedtuple
import csv
from os import path

from .._utils import make_semver


URLS_FILE = urls_file = path.join(path.dirname(__file__), "urls.csv")

UrlLineItem = namedtuple("UrlLineItem", [
    "major",
    "minor",
    "patch",
    "os",
    "os_version",
    "url",
])


def read_urls_file(urls_file):
    lines = []
    with open(urls_file) as f:
        reader = csv.reader(f)
        for line_item in reader:
            lines.append(line_item)
    return lines


def make_url_tree(lines):
    url_tree = {}
    for line_item in lines:
        line = UrlLineItem(*line_item)
        major = url_tree.get(int(line.major), {})
        minor = major.get(int(line.minor), {})
        patch = minor.get(int(line.patch), {})
        _os = patch.get(line.os, {})

        _os[line.os_version] = line.url
        patch[line.os] = _os
        minor[int(line.patch)] = patch
        major[int(line.minor)] = major.get(int(line.minor), {})
        url_tree[int(line.major)] = major

    return url_tree


def _closest_uptodate_version_branch(url_tree, major=None, minor=None, patch=None):
    if major not in url_tree.keys():
        major = max(url_tree.keys())
        minor = max(url_tree[major].keys())
        patch = max(url_tree[major][minor].keys())
    else:
        if minor not in url_tree[major].keys():
            minor = max(url_tree[major].keys())
            patch = max(url_tree[major][minor].keys())
        else:
            if patch not in url_tree[major][minor].keys():
                patch = max(url_tree[major][minor].keys())
    return url_tree[major][minor][patch]


def best_url(url_tree, version=None, os_name=None, os_ver=None):
    """
    - if a version is given find closest match that is at least higher version
    - if os_name is not given assume Linux
    - if os_name not found raise exception
    - if os_version is not given or not found find highest version
    - if only one os version is there then return that version
    """
    if version is not None:
        version_branch = _closest_uptodate_version_branch(
            url_tree, *make_semver(version)
        )
    else:
        version_branch = _closest_uptodate_version_branch(url_tree)

    print(version_branch)


if __name__ == "__main__":
    lines = read_urls_file(URLS_FILE)
    url_tree = make_url_tree(lines)
    best_url(url_tree)
