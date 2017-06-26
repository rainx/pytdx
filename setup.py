#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='pytdx',
      version='1.4',
      description='A Python Interface to TDX protocol',
      author='RainX<Jing Xu>',
      author_email='i@rainx.cc',
      url='http://www.zhikuang.org',
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