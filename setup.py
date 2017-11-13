#!/usr/bin/env python
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
VERSION = open(os.path.join(here, 'VERSION')).read().strip()

required_eggs = [
    'python-twitter>=3.3',
    'boto3>=1.4.7',
    'PyYAML>=3.12',
    'awstwitter>=1.0.2'
]

setup(
    name='src.twitter_handler',
    version=VERSION,
    description="",
    author="hrishi",
    author_email='bakshi.hrishikesh@gmail.com',
    url='',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    # http://pythonhosted.org/distribute/setuptools.html#namespace-packages
    namespace_packages=['src'],
    # TODO amb
    include_package_data=True,
    package_data={'src': ['*.yaml', 'static/*.*', 'templates/*.*']},
    install_requires=required_eggs,
    extras_require=dict(
        test=required_eggs + [
            'pytest>=3.2',
        ],
        develop=required_eggs + [
            'ipdb>=0.10.2',
        ]),
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'index=src.twitter_handler:search_and_store'
        ],
    },
    dependency_links=[
    ],
)
