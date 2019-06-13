try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

from mdc import __version__

if not __version__ or __version__ == "<VERSION>":
    raise RuntimeError("Package version not set!")

with open("./README.rst", "r") as fh:
    LONG_DESCRIPTION = fh.read()

with open("./LICENSE.txt", "r") as fh:
    LICENSE = fh.read()

setup(
    name="mdc",
    author="Aljosha Friemann",
    author_email="a.friemann@automate.wtf",
    description="Mapped Diagnostic Context (MDC) library for python",
    url="https://github.com/afriemann/mdc",
    download_url="",
    keywords=["logging", "mdc", "context"],
    version=__version__,
    license=LICENSE,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    install_requires=["future"],
    classifiers=[],
    packages=find_packages(exclude=("test*", "assets")),
    platforms=[],
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
