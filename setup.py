#!/usr/bin/env python3

from pathlib import Path

from setuptools import find_packages, setup

THIS_DIR = Path(__file__).parent


def get_requirements():
    requirements_path = THIS_DIR / "requirements.txt"
    with open(requirements_path) as f:
        requirements = f.read().splitlines()
    return requirements


setup(
    name="benkpress",
    version="0.1.3",
    description="PyQt/PDFJs GUI for creating and evaluating classifiers for PDF"
    "file/page/sentence targets using sklearn compatible pipelines",
    long_description=open(THIS_DIR / "README.md").read(),
    long_description_content_type="text/markdown",
    author="Dennis Hedback",
    author_email="d.hedback@gmail.com",
    url="https://github.com/dennishedback/benkpress",
    packages=find_packages(),
    package_data={"benkpress.resources": ["*.pdf"]},
    install_requires=get_requirements(),
    entry_points={
        "console_scripts": [
            "benkpress=benkpress.application:main",
            "benkpress-filter-sample=benkpress.scripts.filter_sample:main",
            "benkpress-merge-datasets=benkpress.scripts.merge_datasets:main",
            "benkpress-convert-dataset=benkpress.scripts.convert_dataset:main",
        ],
        "benkpress_plugins.page_filters": [
            "Passthrough=benkpress.plugin:PassthroughPageClassifier",
        ],
        "benkpress_plugins.pipelines": [
            "Dummy=benkpress.plugin:DummyPipeline",
            "TfidfXgboost=benkpress.plugin:tfidf_xgb_pipeline",
            "TfidfSvSmoteXgboost=benkpress.plugin:tfidf_sv_smote_xgb_pipeline",
        ],
    },
)
