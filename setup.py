#!/usr/bin/env python3

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

dependencies = ["pandas", "docopt", "sklearn", "PyQt5", "joblib", "PyPDF2", "PyQtWebEngine"]

setup(
    name="PDFSupervisors",
    version="0.1.0",
    description="PyQt/PDFJs GUI for creating and evaluating classifiers for PDF file/page/sentence targets using sklearn compatible pipelines",
    url="https://github.com/dennishedback/pdfsupervisors",
    author="Dennis Hedback",
    author_email="d.hedback@gmail.com",
    packages=["pdfsupervisors"],
    license="BSD 2-Clause",
    install_requires=dependencies,
    #test_suite="tests.test",
    long_description=open("README.md").read(),
    python_requires=">=3.0.*",
    entry_points={
        'console_scripts': [
            'pdfsupervisors=pdfsupervisors.main:main'
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD 2-Clause",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)