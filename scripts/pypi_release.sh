#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && cd .. && pwd )"
cd $DIR

# Delete old build
rm -rf build dist > /dev/null

# Create new source and binary build
python3 setup.py sdist bdist_wheel

if [ "$1" = "--release" ]; then
  # Upload to PyPI
  python3 -m twine upload dist/*
else
  # Upload to test PyPI
  python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
fi
