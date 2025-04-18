#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="qdown",
    version="1.0.0",
    description="Client for QualitegDrive",
    author="Qualiteg Inc.",
    author_email="qualiteger@qualiteg.com",
    url="https://github.com/qualiteg/qdown",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.23.0",
        "tqdm>=4.64.0",
    ],
    entry_points={
        "console_scripts": [
            "qdown=qdown.gdown:main",  # ファイル名をgdown.pyに修正
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
)