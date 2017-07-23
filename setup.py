#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pytdx',
    version='1.9',
    description='A Python Interface to TDX protocol',
    author='RainX<Jing Xu>',
    author_email='i@rainx.cc',
    url='https://github.com/rainx/pytdx',
    packages=find_packages(),
    install_requires=[
          'click',
          'pandas',
          'six'
    ],
    entry_points={
          'console_scripts': [
              'hqget=pytdx.bin.hqget:main'
          ]
      }
    )

