#!/bin/bash
# Setup dependencies for TRAVIS

brew update
brew install swig
if [ ${PYTHON_VERSION} == "2.7" ];
then
    brew install python;
    pip install wheel
fi
if [ ${PYTHON_VERSION} == "3.4" ];
then
    brew install python3;
    pip3 install wheel
fi
