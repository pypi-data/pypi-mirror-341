#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" setup.py for pypi """

import os
import setuptools
from egos_helpers import constants

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = constants.VERSION

if constants.BUILD:
    version += f'.{constants.BUILD}'

requirement_path = f"{os.path.dirname(os.path.realpath(__file__))}/requirements.txt"
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path, 'r', encoding='utf8') as f:
        install_requires = f.read().splitlines()

setuptools.setup(version=version)
