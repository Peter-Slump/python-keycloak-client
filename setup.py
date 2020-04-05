import os
import sys

from setuptools import find_packages, setup

VERSION = '0.2.3'
AIO_COMPATIBLE = sys.version_info >= (3, 5, 3)

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

EXCLUDED_PACKAGES = []
TESTS_REQUIRE = [
    'pytest',
    'pytest-cov',
    'mock>=2.0',
]

if AIO_COMPATIBLE:
    TESTS_REQUIRE += [
        'asynctest',
    ]
else:
    EXCLUDED_PACKAGES.append('keycloak.aio')

setup(
    name='python-keycloak-client',
    version=VERSION,
    long_description=README,
    package_dir={'': 'src'},
    packages=find_packages('src', EXCLUDED_PACKAGES),
    extras_require={
        'dev': [
            'bumpversion==0.5.3',
            'twine',
        ],
        'doc': [
            'Sphinx==1.4.4',
            'sphinx-autobuild==0.6.0',
        ],
        'aio': [
            'aiohttp>=3.4.4,<4; python_full_version>="3.5.3"'
        ]
    },
    setup_requires=[
        'pytest-runner>=4.0,<5'
    ],
    install_requires=[
        'requests',
        'python-jose',
    ],
    tests_require=TESTS_REQUIRE,
    url='https://github.com/Peter-Slump/python-keycloak-client',
    license='MIT',
    author='Peter Slump',
    author_email='peter@yarf.nl',
    description='Install Python Keycloak client.',
    classifiers=[]
)
