#!/bin/bash

PYTHON_EXE_PATH=

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

PYTHONPATH=$SCRIPT_DIR \
"${PYTHON_EXE_PATH}python" -O $SCRIPT_DIR/DemoStandAloneApp.pyz