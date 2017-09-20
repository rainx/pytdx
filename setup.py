#!/usr/bin/env python

from setuptools import setup, find_packages
import os

PYTDX_CYTHON = os.getenv("PYTDX_CYTHON", None)

if PYTDX_CYTHON:
    from Cython.Build import cythonize
    cythonkw = {
        "ext_modules": cythonize("pytdx/reader/c_gbbq_reader.pyx")
    }
else:
    cythonkw = {}
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ''


setup(
    name='pytdx',
    version='1.43',
    description='A Python Interface to TDX protocol',
    long_description=long_description,
    author='RainX<Jing Xu>',
    author_email='i@rainx.cc',
    url='https://github.com/rainx/pytdx',
    packages=find_packages(),
    install_requires=[
            'click',
            'pandas',
            'six',
            'cryptography'
    ],
    entry_points={
          'console_scripts': [
              'hqget=pytdx.bin.hqget:main',
              'hqreader=pytdx.bin.hqreader:main'

          ]
      },
    **cythonkw
    )

