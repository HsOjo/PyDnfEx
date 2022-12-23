#!/bin/bash
rm -fr dist
python setup.py sdist bdist_wheel
rm -fr build *.egg-info

if [[ $1 = '--upload' ]]; then
  twine upload dist/*
fi
