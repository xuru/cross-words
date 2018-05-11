#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import xwords

# Calling setup with all its parameters
setup(
    name='cross-words',
    version="0.0.1",
    packages=find_packages(),
    author="Clément Choukroun, Alexandre Mourachko",
    author_email="clement.choukroun@ubisoft.com",
    description="Chat bot sentences & story generator.",
    long_description=open('README.md').read(),
    include_package_data=True,
    license='MIT',
    url='https://github.com/data-chirps/xwords',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Communications",
    ]

)
