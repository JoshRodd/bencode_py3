#!/usr/bin/env python3
#
# Copyright (c) 2010 BitTorrent Inc.
#
# Copyright (c) 2017 Josh Rodd

from setuptools import setup, find_packages

setup(
    name = "bencode_py3",
    version = "1.1329139002",
    packages = find_packages(),

    # metadata for upload to PyPI
    author = "Josh Rodd",
    author_email = "josh@rodd.us",
    description = "The BitTorrent bencode module as light-weight, standalone package, ported to Python 3",
    license = "BitTorrent Open Source License",
    keywords = "bittorrent bencode bdecode python3 bencode_py3",
    url = "http://github.com/JoshRodd/bencode_py3",
    zip_safe = True,
    test_suite = "test.testbencode",
    long_description = """This package simply re-packages the existing bencoding and bdecoding implemention from the 'official' BitTorrent client as a separate, light-weight package for re-using them without having the entire BitTorrent software as a dependency, and then has been ported to Python 3.
""",
)
