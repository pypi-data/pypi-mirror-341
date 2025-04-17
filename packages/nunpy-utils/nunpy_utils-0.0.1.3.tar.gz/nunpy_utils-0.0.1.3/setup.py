import os
from setuptools import setup, find_packages

def read(fname):
    r"""Reads a file and returns its content as a string."""
    return open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8").read()

def get_version(rel_path):
    r"""Gets the version of the package from the __init__ file."""
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]

    raise RuntimeError("Unable to find version string.")

setup(
    name="nunpy-utils",
    version=get_version("nunpy/__init__.py"),
    author="Giacomo Nunziati",
    url="https://github.com/nunziati/nunpy",
    author_email="giacomo.nunziati.0@gmail.com",
    license="MIT License",
    description="Yet another utility library for Python",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
    ],
)
