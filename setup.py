# -*- coding: utf-8 -*-

import os
import pip

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

from mdc import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), 'r').read()


INSTALL_REQS = pip.req.parse_requirements(
    'requirements.txt',
    session=pip.download.PipSession()
)

REQUIREMENTS = [str(ir.req) for ir in INSTALL_REQS if ir is not None]

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
    install_requires=REQUIREMENTS,
    classifiers=[],
    packages=find_packages(exclude=('test*', 'assets')),
    platforms=[]
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
