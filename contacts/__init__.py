from flask import *
from flask_oauthlib.client import OAuth, OAuthException

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('contacts.default_config')
# app.config.from_envvar('SIM_CONTACTS_SETTINGS')
app.config.from_pyfile('config.py')


app.secret_key = app.config.get('SECRET_KEY', "DEV TESTING")



from . import views
from . import model
from . import auth
