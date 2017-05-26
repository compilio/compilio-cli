#!/usr/bin/env python

from setuptools import setup, find_packages

VERSION = '0.1.2'

install_requires = ['PyYAML', 'requests']

setup(
    name='compilio-cli',
    version=VERSION,
    description='CLI tool to interact with Compilio API',
    author='Quentin de Longraye',
    url='https://github.com/compilio/compilio-cli',
    license='GPL',
    packages=find_packages(),
    install_requires=install_requires,
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
