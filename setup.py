import os

import setuptools
from mypyc.build import mypycify

SRC_DIR = "./src"


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), "rt", encoding="utf-8") as file:
        return file.read()


setuptools.setup(
    name="PyVarint",
    version="0.0.1",
    description="Varint encoding and decoding algorithms writen on Python",
    author="Alexey Belkov",
    author_email="alexey.belkov@gmail.com",
    url="https://github.com/xenolex/PyVarInt",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license="License :: OSI Approved :: Apache Software License 2.0",
    ext_modules=mypycify([os.path.join(SRC_DIR, "VarInt.py"),
                          os.path.join(SRC_DIR, "utils.py")], opt_level="3", debug_level="1")
)