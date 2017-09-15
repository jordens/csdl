#!/usr/bin/python
# -*- coding: utf8 -*-
#
#   csdl - Cross Stitched Spectral Density
#   Copyright (C) 2017 Robert Jordens <jordens@gmail.com>

from __future__ import (absolute_import, division, unicode_literals,
        print_function)

from setuptools import setup, find_packages

setup(
    name="csdl",
    description="Cross Stiched Spectral Density",
    version="0.1",
    author="Robert Jordens",
    author_email="jordens@gmail.com",
    url="https://github.com/jordens/csdl",
    license="BSD",
    install_requires=["numpy", "matplotlib", "scipy"],
    packages = find_packages(),
)
