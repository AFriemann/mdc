# -*- coding: utf-8 -*-

import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

from mdc import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), 'r').read()


if not __version__ or __version__ == '<VERSION>':
    raise RuntimeError("Package version not set!")

setup(
    name="mdc",
    author="Aljosha Friemann",
    author_email="a.friemann@automate.wtf",
    description="Mapped Diagnostic Context (MDC) library for python",
    url="https://github.com/afriemann/mdc",
    download_url="",
    keywords=['logging', 'mdc'],
    version=__version__,
    license=read('LICENSE.txt'),
    long_description=read('README.rst'),
    install_requires=[],
    classifiers=[],
    packages=find_packages(exclude=('test*', 'assets')),
    platforms=[]
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
