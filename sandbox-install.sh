#!/bin/bash

rm -rf tst || true
mkdir tst
pushd tst
# test installation of module in virtual environment
virtualenv my-printex-venv
source my-printex-venv/bin/activate

pip3 install printex
python3 ../test.py
deactivate

popd tst
