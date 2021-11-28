#!/bin/bash

PYTHON_EXE_PATH=

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

LIB_PATH="${SCRIPT_DIR}/LIBS"

PYTHONPATH=$SCRIPT_DIR \
"${PYTHON_EXE_PATH}python" -O $SCRIPT_DIR/MyPackage.pyz