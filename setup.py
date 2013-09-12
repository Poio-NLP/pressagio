# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2001-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://www.cidles.eu/ltll/poio>
# For license information, see LICENSE.TXT

import os

# Use the VERSION file to get version
version_file = os.path.join(os.path.dirname(__file__), 'src', 'pressagio', 'VERSION')
with open(version_file) as fh:
    pressagio_version = fh.read().strip()

import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name = "pressagio",
    description = "A Python Library for text prediction.",
    version = pressagio_version,
    url = "https://github.com/cidles/pressagio",
    #download_url = "http://media.cidles.eu/poio/poio-api/",
    #long_description = "Python implementation of the Graph Annotation Framework. (http://www.americannationalcorpus.org/graf-wiki)",
    license = "Apache License, Version 2.0",
    keywords = ['NLP', 'CL', 'natural language processing',
                'computational linguistics', 'parsing', 'tagging',
                'text prediction', 'linguistics', 'language',
                'natural language'],
    maintainer = "Peter Bouda",
    maintainer_email = "pbouda@cidles.eu",
    author = "Peter Bouda",
    author_email = "pbouda@cidles.eu",
    classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Human Machine Interfaces',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: General',
    'Topic :: Text Processing :: Indexing',
    'Topic :: Text Processing :: Linguistic',
    ],
    packages = [ 'pressagio', 'pressagio.core' ],
    package_dir = { '': 'src' },
    package_data = { 'pressagio': ['VERSION'] },
)
