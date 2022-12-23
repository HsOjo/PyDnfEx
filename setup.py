#!/usr/bin/env python
import setuptools

from pydnfex.const import Const

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
    name="PyDnfEx",
    version=Const.version,
    author="HsOjo",
    author_email="hsojo@qq.com",
    keywords='python3 dnf',
    description='''A data pack extract lib for Dungeon & Fighter.''',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HsOjo/PyDnfEx/",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    python_requires='>=3.7',
    install_requires=requirements,
)
