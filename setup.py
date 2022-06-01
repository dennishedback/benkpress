#!/usr/bin/env python3

import os
from setuptools import setup

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

setup(
    name="PDFSupervisors",
    version="0.1.0",
    description="PyQt/PDFJs GUI for creating and evaluating classifiers for PDF file/page/sentence targets using sklearn compatible pipelines",
    long_description=open(os.path.join(THIS_DIR, "README.md")).read(),
    long_description_content_type="text/markdown",
    author="Dennis Hedback",
    author_email="d.hedback@gmail.com",
    url="https://github.com/dennishedback/pdfsupervisors",
    packages=["pdfsupervisors"],
    install_requires=[
        "imbalanced-learn",
        "joblib",
        "numpy",
        "pandas",
        "PyPDF2",
        "PyQt5",
        "PyQtWebEngine",
        "sklearn",
        "xgboost",
    ],
    entry_points={
        "console_scripts": ["pdfsupervisors=pdfsupervisors.main:main"],
    },
)
