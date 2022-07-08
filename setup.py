"""Python setup.py for learn_raft package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("learn_raft", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="learn_raft",
    version=read("learn_raft", "VERSION"),
    description="Distributed gRPC driven KV store written in python for learning Raft",
    url="https://github.com/arunma/learn_raft/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="arunma",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["learn_raft = learn_raft.cli:cli"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)
