#!/usr/bin/env python

from setuptools import setup

VERSION = '0.1.0'

setup(
    pbr=True,
    version=VERSION,
    entry_points={
        'console_scripts': [
            'compilio=compilio.cli:main'
        ],
    }
)
