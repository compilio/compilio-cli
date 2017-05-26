#!/usr/bin/env python

from setuptools import setup

setup(
    pbr=True,
    entry_points={
        'console_scripts': [
            'compilio=compilio.cli:main'
        ],
    }
)
