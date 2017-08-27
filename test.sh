#!/bin/bash

if [[ "$VIRTUAL_ENV" == "" ]]; then
    virtualenv .env
    . env/bin/activate
fi

pip install -r requirements-dev.txt

nosetests

