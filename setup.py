import os
import io
from os.path import dirname
from os.path import join

from setuptools import find_packages, setup

VERSION = "0.2.4-dev"


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")
    ) as fh:
        return fh.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name="python-keycloak-client",
    version=VERSION,
    long_description=read("README.rst"),
    package_dir={"": "src"},
    packages=find_packages("src"),
    extras_require={
        "dev": ["bumpversion==0.5.3", "twine", "black", "mypy"],
        "doc": ["Sphinx==1.4.4", "sphinx-autobuild==0.6.0"],
        "aio": ['aiohttp>=3.4.4,<4; python_full_version>="3.5.3"'],
    },
    setup_requires=["pytest-runner>=4.0,<5"],
    install_requires=["requests", "python-jose"],
    tests_require=["pytest", "pytest-cov", "asynctest"],
    url="https://github.com/Peter-Slump/python-keycloak-client",
    license="MIT",
    author="Peter Slump",
    author_email="peter@codecraft.nl",
    description="Install Python Keycloak client.",
    classifiers=[],
)
