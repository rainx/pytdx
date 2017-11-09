#!/usr/bin/env python

from setuptools import setup, find_packages
import os

PYTDX_CYTHON = os.getenv("PYTDX_CYTHON", None)

if PYTDX_CYTHON:
    from Cython.Build import cythonize
    cythonkw = {
        "ext_modules": cythonize(
            ["pytdx/reader/c_gbbq_reader.pyx",
             'pytdx/parser/get_security_quotes.py',
             'pytdx/parser/base.py',
             'pytdx/helper.py',
             'pytdx/hq.py',
             'pytdx/base_socket_client.py',
             ])
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
    version='1.56',
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
            'cryptography',
    ],
    entry_points={
          'console_scripts': [
              'hqget=pytdx.bin.hqget:main',
              'hqreader=pytdx.bin.hqreader:main',
              'get_tts=pytdx.bin.get_tdx_trader_server:main',
              'hqbenchmark=pytdx.bin.hqbenchmark:main',
          ]
      },
    **cythonkw
    )

