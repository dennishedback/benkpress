#!/usr/bin/env python3

import os

from setuptools import setup

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

setup(
    name="benkpress",
    version="0.1.1",
    description="PyQt/PDFJs GUI for creating and evaluating classifiers for PDF"
    "file/page/sentence targets using sklearn compatible pipelines",
    long_description=open(os.path.join(THIS_DIR, "README.md")).read(),
    long_description_content_type="text/markdown",
    author="Dennis Hedback",
    author_email="d.hedback@gmail.com",
    url="https://github.com/dennishedback/benkpress",
    packages=["benkpress"],
    install_requires=[
        "benkpress-plugin-api @ git+https://git@github.com/dennishedback/benkpress-plugin-api.git",
        "pandas>=1.4.2",
        "numpy>=1.22.4",
        "PyPDF2",
        "PyQt5",
        "PyQtWebEngine",
        "sklearn",
        "docopt",
        "appdirs",
    ],
    entry_points={
        "console_scripts": [
            "benkpress=benkpress.main:main",
            "benkpress-filter-sample=benkpress.sample:_filter_sample_main",
            "benkpress-merge-datasets=benkpress.dataset:_merge_datasets_main",
        ],
    },
)
