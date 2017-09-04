if [ ! -f .env/bin/activate ]; then
    virtualenv .env
fi
. .env/bin/activate
pip install -r requirements.txt

export FLASK_APP=contacts
export FLASK_DEBUG=1
# export SIM_CONTACTS_SETTINGS=settings.cfg
export SIM_CONTACTS_SETTINGS=config.py

python2 -m flask run

