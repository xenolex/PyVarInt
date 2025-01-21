import os

import setuptools
from mypyc.build import mypycify

__version__ = "1.0.0"

BUILD_DIR = "./PyVarInt"


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), "rt", encoding="utf-8") as file:
        return file.read()


setuptools.setup(
    name="PyVarInt",
    packages=["PyVarInt"],
    version=__version__,
    description="Varint encoding and decoding algorithms writen on Python",
    author="Alexey Belkov",
    author_email="alexey.belkov@gmail.com",
    url="https://github.com/xenolex/PyVarInt",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license="License :: OSI Approved :: Apache Software License 2.0",
    ext_modules=mypycify([
        os.path.join(BUILD_DIR, "__init__.py"),
        os.path.join(BUILD_DIR, "algorithms.py"),
    ],
        opt_level="3", debug_level="1")
)
