#!/usr/bin/env bash 

#
# 构建基础的开发环境 (For mac)
#

# If virtualenv not installed, install it first
which virtualenv
if [ ! $? == 0 ]; then
    pip install virtualenv
fi

if [ ! -d ./env ]; then
    virtualenv env
fi

if [ -d ./env ]; then
    source env/bin/activate
fi

# Install all requirements.txt 
pip install -r requirement-dev.txt

if [ "$(uname)"=="Darwin" ]; then
    brew install pandoc
fi

# Install local
python setup.py develop