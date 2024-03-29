#!/bin/bash

if [ ! -f .env/bin/activate ]; then
    python3 -m venv .env
fi
. .env/bin/activate
pip install -r requirements.txt

export FLASK_APP=contacts
export FLASK_DEBUG=1
# export SIM_CONTACTS_SETTINGS=settings.cfg
export SIM_CONTACTS_SETTINGS=config.py

echo "Run this: open http://localhost:5000"
python3 -m flask run $*

