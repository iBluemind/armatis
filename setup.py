from armatis import __version__ as armatis_current_version
from setuptools import setup, find_packages
from codecs import open
from os import path
import unittest

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def armatis_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite

setup(
    name='armatis',
    version=armatis_current_version,
    description='Armatis parses the website or web API response of Korean parcel'
                ' delivery service company for tracking the parcel.',
    long_description=long_description,
    url='https://github.com/iBluemind/armatis',
    author='Han Manjong',
    author_email='han@manjong.org',
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='parcel delivery korea',
    packages=find_packages(exclude=['sphinx', 'docs', 'tests']),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml',
        'six'
    ],
    tests_require=['mock'],
    test_suite='setup.armatis_test_suite'
)
