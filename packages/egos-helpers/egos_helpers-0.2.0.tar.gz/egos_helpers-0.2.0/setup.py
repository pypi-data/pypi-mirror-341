#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" setup.py for pypi """

import setuptools
from egos_helpers.constants import NAME, BUILD, VERSION

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = VERSION

if BUILD:
    version += f'.{BUILD}'

setuptools.setup(
    name=NAME,
    version=version,
    author="Alex Thomae",
    author_email="egos-helpers@egos.tech",
    description="A python library for helper functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT License',
    license_files=['LICENSE'],
    url="https://gitlab.com/egos-tech/egos-helpers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
