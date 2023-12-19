#!/bin/bash

if [[ "$VIRTUAL_ENV" == "" ]]; then
  if [ ! -d .env ]; then
    python3 -m venv .env
  fi
  . .env/bin/activate
fi

pip install -qr requirements-dev.txt

mkdir -p instance
touch instance/config.py

cat <<EOF > instance/test.py
FACEBOOK_APP_ID = "TEST"
FACEBOOK_APP_SECRET = "TEST"
SECRET_KEY = 'test'
SQLALCHEMY_DATABASE_URI = "sqlite://"
EOF


export SIM_CONTACTS_SETTINGS=test.py

python3 -m pytest --ignore=vue --ignore=node_modules

