from collections import namedtuple
import logging

from .._utils import make_semver
from ._patterns import URLS


logger = logging.getLogger("PYMONGOIM_DOWNLOAD_URL")

ExpandedURL = namedtuple("ExpandedURL", [
    "os_name",
    "os_version",
    "version",
    "url"
])


class OperatingSystemNameNotFound(ValueError):
    pass


class OperatingSystemVersionNotFound(ValueError):
    pass


def best_url(os_name, version=None, os_ver=None, url_tree=None):
    if url_tree is None:
        url_tree = URLS

    try:
        os_branch = url_tree[str(os_name).lower()]
    except KeyError:
        raise OperatingSystemNameNotFound(
            "Can't find a MongoDB for this OS: {}".format(os_name))

    if os_ver is None:
        os_ver = max(os_branch.keys())
    else:
        os_ver = str(os_ver).lower()

    os_ver = str(os_ver)
    if os_ver not in os_branch.keys():
        raise OperatingSystemVersionNotFound(
            (
                "Can't find a MongoDB for OS {} "
                "version {}, available OS versions: {}"
            ).format(
                os_name, os_ver, os_branch.keys())
            )

    version_branch = os_branch[os_ver]

    major, minor, patch = make_semver(version)
    if major not in version_branch.keys():
        major = max(version_branch.keys())
        minor = max(version_branch[major].keys())
        patch = max(version_branch[major][minor]["patches"])
    elif minor not in version_branch[major].keys():
        minor = max(version_branch[major].keys())
        patch = max(version_branch[major][minor]["patches"])
    elif patch not in version_branch[major][minor]["patches"]:
        patch = max(version_branch[major][minor]["patches"])

    logger.info("Requested MongoDB version {}, found version: {}.{}.{}".format(
        version, major, minor, patch
    ))
    version = "{}.{}.{}".format(major, minor, patch)
    return version_branch[major][minor]["url"].format(version)


def expand_url_tree(tree):
    for os_name, os_leaf in tree.items():
        for os_version, version_leaf in os_leaf.items():
            for major, major_leaf in version_leaf.items():
                for minor, minor_leaf in major_leaf.items():
                    for patch in minor_leaf["patches"]:
                        version = "{}.{}.{}".format(major, minor, patch)
                        yield ExpandedURL(
                            os_name,
                            os_version,
                            version,
                            minor_leaf["url"].format(version)
                        )
