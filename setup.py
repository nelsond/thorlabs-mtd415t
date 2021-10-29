# -*- coding: utf-8 -*-
from setuptools import setup
import os
from thorlabs_mtd415t.version import __version__

current_path = os.path.dirname(os.path.abspath(__file__))

# Get the long description from the README file
with open(os.path.join(current_path, 'README.md')) as f:
    long_description = f.read()

with open(os.path.join(current_path, 'requirements', 'common.txt')) as f:
    required = f.read().splitlines()

setup(
    name='thorlabs-mtd415t',

    version=__version__,

    description='Simple wrapper for the Thorlabs MTD415T OEM '
                'temperature controller module.',
    long_description=long_description,

    url='https://github.com/nelsond/thorlabs-mtd415t',

    author='Nelson Darkwah Oppong',
    author_email='n@darkwahoppong.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Stable',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='mtd415t temperature controller serial',

    packages=['thorlabs_mtd415t'],

    install_requires=required
)
