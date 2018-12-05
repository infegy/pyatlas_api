#!/usr/bin/env python

from setuptools import setup

setup(name='Atlas API',
      version='1.0',
      description='Python library for interacting with the Infegy Atlas API',
      author='Infegy, Inc.',
      author_email='support@infegy.com',
      install_requires=['requests', 'python-dateutil'],
      url='https://atlas.infegy.com',
      py_modules=['atlas_api'])
