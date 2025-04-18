#!/usr/bin/env python
# setup.py
from setuptools import setup, find_packages

setup(
    name="satquest",
    version="0.1.0-alpha",
    author="你的名字",
    author_email="you@example.com",
    description="SATQuest",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sdpkjc/SATQuest",
    packages=find_packages('.'),
    python_requires=">=3.9",
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
