#!/bin/bash

. ./venv/bin/activate
pushd ./src >/dev/null
python3 -m app
popd >/dev/null

