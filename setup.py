#!/usr/bin/env python3

import os

from setuptools import setup

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

setup(
    name="benkpress",
    version="0.1.2",
    description="PyQt/PDFJs GUI for creating and evaluating classifiers for PDF"
    "file/page/sentence targets using sklearn compatible pipelines",
    long_description=open(os.path.join(THIS_DIR, "README.md")).read(),
    long_description_content_type="text/markdown",
    author="Dennis Hedback",
    author_email="d.hedback@gmail.com",
    url="https://github.com/dennishedback/benkpress",
    packages=["benkpress", "benkpress.api", "benkpress.scripts"],
    install_requires=[
        "pandas>=1.4.2",
        "numpy>=1.22.4",
        "pdf2image",
        "pytesseract",
        "PyQt5",
        "PyQtWebEngine",
        "PyPDF2<=2.12.1",
        "scikit-learn",
        "docopt",
        "appdirs",
    ],
    entry_points={
        "console_scripts": [
            "benkpress=benkpress.application:main",
            "benkpress-filter-sample=benkpress.scripts.filter_sample:main",
            "benkpress-merge-datasets=benkpress.scripts.merge_datasets:main",
        ],
    },
)
