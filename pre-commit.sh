VIRTUAL_ENV=/Users/ed/dev/contacts-python/.env

if [[ "$VIRTUAL_ENV" == "" ]]; then
  if [ ! -d .env ]; then
    virtualenv .env
  fi
  . .env/bin/activate
fi
pip install -r requirements-dev.txt
python -m pytest
