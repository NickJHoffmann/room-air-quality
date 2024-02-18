#!/bin/bash

LOGS="${1:-logs}"
FILES=$(find src -type f -name '*.py')
pylint --disable=logging-fstring-interpolation ${FILES}
