#!/bin/bash

PYTHON_EXE_PATH=""
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd $SCRIPT_DIR

BUILD_CONFIG_PATH=$SCRIPT_DIR

PYTHONPATH=$BUILD_CONFIG_PATH \
BUILD_CONFIG="$BUILD_CONFIG_PATH/BuildConfig.json" \
"${PYTHON_EXE_PATH}python" -O $BUILD_CONFIG_PATH/PyCompilePackager.pyz