#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" setup.py for pypi """

import os
import setuptools
try:
    from egos_helpers.constants import VERSION, BUILD
except ModuleNotFoundError:
    VERSION = '0.3.4'
    BUILD = '1'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = VERSION

if BUILD:
    version += f'.{BUILD}'

requirement_path = f"{os.path.dirname(os.path.realpath(__file__))}/requirements.txt"
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path, 'r', encoding='utf8') as f:
        install_requires = f.read().splitlines()

setuptools.setup(version=version)
