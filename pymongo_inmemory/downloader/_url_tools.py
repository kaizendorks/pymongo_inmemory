from collections import namedtuple
import csv
from os import path
from pprint import pprint


UrlLineItem = namedtuple("UrlLineItem", [
    "major",
    "minor",
    "patch",
    "os",
    "os_version",
    "url",
])


if __name__ == "__main__":
    urls_file = path.join(path.dirname(__file__), "urls.csv")
    url_tree = {}

    with open(urls_file) as f:
        reader = csv.reader(f)
        for line_item in reader:
            line = UrlLineItem(*line_item)
            major = url_tree.get(line.major, {})
            minor = major.get(line.minor, {})
            patch = minor.get(line.patch, {})
            _os = patch.get(line.os, {})
            _os[line.os_version] = line.url
            patch[line.os] = _os
            minor[line.patch] = patch
            major[line.minor] = major.get(line.minor, {})
            url_tree[line.major] = major

    pprint(url_tree)
