#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='pytdx',
      version='1.0',
      description='A Python Interface to TDX protocol',
      author='RainX',
      author_email='i@rainx.cc',
      url='https://www.zhikuang.org',
      packages=find_packages(),
      install_requires=[
          'click',
      ],
      entry_points={
          'console_scripts': [
              'hqget=pytdx.bin.hqget:main'
          ]
      }

      )