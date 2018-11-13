#!/bin/bash

dir=$(dirname $0)

# flake8 (runs pep8 and pyflakes)
flake8 .
if [ $? -ne 0 ]; then
    echo "Exiting due to flake8 errors. Fix and re-run to finish tests."
    exit $?
fi

# pylint
output=$(pylint $dir/hairball 2> /dev/null)
if [ -n "$output" ]; then
    echo "--pylint--"
    echo -e "$output"
fi

# pep257
find $dir -name [A-Za-z_]\*.py | xargs pep257

exit 0