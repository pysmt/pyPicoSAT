#!/bin/bash

PICOSAT_DIR=$1
PYTHON=`which python`
#PYTHON=`which python3.5`
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ "X${PICOSAT_DIR}" == "X" ]; then
    echo "Usage: ./build.sh <picosat_dir>"
    exit 1
fi

cd $PICOSAT_DIR
export CFLAGS=" -fPIC"
sh configure
make

cd $DIR
# SWIG (swig is handled within setup.py)
# swig -I${PICOSAT_DIR} -python -o picosat_python_wrap.c picosat_python.i
# Build
$PYTHON ./setup.py build

# PKG (This is done by travis-CI. It is left here for reference)
# $PYTHON ./setup.py egg_info --tag-date --tag-build=.dev bdist_wheel
