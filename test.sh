#!/bin/bash

if [[ "$VIRTUAL_ENV" == "" ]]; then
  if [ ! -d .env ]; then
    virtualenv .env
  fi
  . .env/bin/activate
fi

pip install -qr requirements-dev.txt

cat <<EOF > instance/test.py
FACEBOOK_APP_ID = "TEST"
FACEBOOK_APP_SECRET = "TEST"
SECRET_KEY = 'test'
EOF


export SIM_CONTACTS_SETTINGS=test.py

python -m pytest

