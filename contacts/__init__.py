from flask import *
from flask_oauthlib.client import OAuth, OAuthException
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('contacts.default_config')
app.config.from_envvar('SIM_CONTACTS_SETTINGS', silent=True)
app.config.from_pyfile('config.py')


app.secret_key = app.config.get('SECRET_KEY', "DEV TESTING")
if app.secret_key == "DEV TESTING":
    print "WARNING: Set a secret key!!!"

toolbar = DebugToolbarExtension(app)


from . import views
from . import model
from . import auth
from .api import api


app.register_blueprint(api, url_prefix="/api")
