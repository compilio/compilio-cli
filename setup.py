#!/usr/bin/env python

from setuptools import setup

VERSION = '0.1.4'

setup(
    name='compilio-cli',
    version=VERSION,
    description='CLI tool to interact with Compilio API',
    long_description=open('README.md').read(),
    author='Quentin de Longraye',
    url='https://github.com/compilio/compilio-cli',
    license='GPL',
    packages=['compilio'],
    package_data={
        'compilio': ['*.yml'],
    },
    install_requires=['PyYAML', 'requests'],
    entry_points="""
    [console_scripts]
    compilio=compilio.cli:main
    """,
    include_package_data=True,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
)
