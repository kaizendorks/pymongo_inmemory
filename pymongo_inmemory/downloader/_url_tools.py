from collections import namedtuple
import csv
from os import path

from .._utils import make_semver


URLS_FILE = urls_file = path.join(path.dirname(__file__), "urls.csv")


class OperatingSystemNameNotFound(ValueError):
    pass


class OperatingSystemVersionNotFound(ValueError):
    pass


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
    """
    - Given `major.minor.patch` version:
        - Starting from `major` to `patch`
        - If there is an exact match take it
        - If there isn't, take the highest and go on with the highest
    """
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


def _url_leaf(version_branch, os_name, os_ver=None):
    # If `os_name` not found raise exception
    if os_name not in version_branch.keys():
        raise OperatingSystemNameNotFound(
            "Can't find a MongoDB for {} for this version".format(os_name))

    os_leaves = version_branch[os_name]

    # If there is only one version return that version
    if len(os_leaves) == 1:
        return list(os_leaves.values())[0]

    # If `os_version` is not given find highest version
    if os_ver is None:
        # `generic` is higher than numeric versions
        os_ver = max(os_leaves.keys())

    # If `os_version` is not found raise exception
    if os_ver not in os_leaves.keys():
        raise OperatingSystemVersionNotFound(
            "Can't find a MongoDB for {} {}, available OS versions: {}".format(
                os_name, os_ver, os_leaves.keys()))

    return os_leaves[os_ver]


def best_url(os_name, version=None, os_ver=None):
    url_tree = make_url_tree(read_urls_file(URLS_FILE))
    if version is not None:
        version_branch = _closest_uptodate_version_branch(
            url_tree, *make_semver(version)
        )
    else:
        version_branch = _closest_uptodate_version_branch(url_tree)

    return _url_leaf(version_branch, os_name, os_ver)
