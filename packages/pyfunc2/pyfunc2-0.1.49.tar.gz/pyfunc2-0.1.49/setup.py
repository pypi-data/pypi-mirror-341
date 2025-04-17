#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Installation of the pyfunc2 package.
"""

import os
from setuptools import setup, find_packages

# Long description from README.md
try:
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"), encoding="utf-8") as f:
        LONG_DESCRIPTION = '\n' + f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = ''

# Configuration setup
setup(
    name="pyfunc2",
    version="0.1.49",
    description="libs for cameramonit, ocr, fin-officer, cfo, and other projects",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Tom Sapletta",
    author_email="tom@sapletta.com",
    maintainer="pyfunc developers",
    maintainer_email="info@softreck.dev",
    python_requires=">=3.7",
    url="https://www.pyfunc.com",
    project_urls={
        "Repository": "https://github.com/pyfunc/lib",
        "Changelog": "https://github.com/pyfunc/lib/releases",
        "Wiki": "https://github.com/pyfunc/lib/wiki",
        "Issue Tracker": "https://github.com/pyfunc/lib/issues/new",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "attrs==25.3.0",
        "Automat==24.8.1",
        "build==1.2.2.post1",
        "certifi==2025.1.31",
        "charset-normalizer==3.4.1",
        "click==8.1.8",
        "constantly==23.10.4",
        "fastjsonschema==2.21.1",
        "gitdb==4.0.12",
        "GitPython==3.1.44",
        "hatchling==1.27.0",
        "hyperlink==21.0.0",
        "idna==3.10",
        "incremental==24.7.2",
        "iniconfig==2.1.0",
        "packaging==24.2",
        "path==17.1.0",
        "pathspec==0.12.1",
        "pluggy==1.5.0",
        "pyproject_hooks==1.2.0",
        "pytest==8.3.5",
        "pytest",
        "pdf2image",
        "wand",
        "pillow",
        "PyPDF2",
        "pypdf",
        "pdfreader",
        "datefinder",
        "numpy",
        "requests==2.32.3",
        "setuptools==78.1.0",
        "six==1.17.0",
        "smmap==5.0.2",
        "stringcase==1.2.0",
        "toml==0.10.2",
        "tomli==2.2.1",
        "trove-classifiers==2025.4.11.15",
        "Twisted==24.11.0",
        "typing_extensions==4.13.2",
        "urllib3==2.4.0"
    ],
    license="Apache-2.0",  # Use simple string format
    license_files=("LICENSE"),  # Empty tuple to explicitly prevent license files
    keywords=["python", "pyfunc", "pyfunc2", "pyfunc3", "pyfunc"],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    # Critical fix for the license-file issue:
    # This prevents setuptools from automatically adding a license-file entry
)