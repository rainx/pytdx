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
    print(30 * "*")
    print("Notice, NEED TO INSTALL *pypandoc* TO get full description of package")
    print(30 * "*")
    long_description = ''

# try get current branch
cur_branch = 'master'
try:
    from git import Repo
    cur_path = os.path.abspath(os.path.dirname(__file__))
    repo = Repo(cur_path)
    cur_branch = repo.active_branch.name

except Exception as e:
    print(30 * "*")
    print("Notice, NEED TO INSTALL *GitPython* TO setup package with branch name")
    print(30 * "*")


pkg_name = 'pytdx'

if cur_branch != 'master':
    pkg_name = 'pytdx-' + cur_branch

print(30 * '-')
print("Current Branch is {}, so package name is {}".format(cur_branch, pkg_name))
print(30 * '-')

setup(
    name=pkg_name,
    version='1.63',
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

