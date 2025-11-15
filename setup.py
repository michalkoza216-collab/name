#!/usr/bin/env python3
"""
Setup script for Product Variant Renaming Tool
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="shopify-variant-renamer",
    version="1.0.0",
    author="Product Variant Renaming Tool Contributors",
    description="AI-powered tool for renaming Shopify product variants",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michalkoza216-collab/name",
    py_modules=["variant_renamer"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "variant-renamer=variant_renamer:main",
        ],
    },
    include_package_data=True,
    keywords="shopify ecommerce csv variant ai openai",
)
