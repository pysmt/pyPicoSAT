#!/bin/bash

PICOSAT_DIR=$1
PYTHON=`which python`
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ "X${PICOSAT_DIR}" == "X" ]; then
    echo "Usage: ./build.sh <picosat_dir>"
    exit 1
fi

cd $PICOSAT_DIR
sh configure -shared
make

cd $DIR
$PYTHON ./setup.py --picosat-dir="$PICOSAT_DIR" build

$PYTHON ./setup.py bdist --picosat-dir="$PICOSAT_DIR"
