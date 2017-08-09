from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth

app = Flask(__name__)
# app.config.from_object('yourapplication.default_settings')
app.config.from_envvar('SIM_CONTACTS_SETTINGS')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://db/dev.sqlite3'
db = SQLAlchemy(app)

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=app.config['FACEBOOK_APP_ID'],
    consumer_secret=app.config['FACEBOOK_APP_SECRET'],
    request_token_params={'scope': 'email'}
)

@app.route('/')
def hello_world():
    return 'Hello, World!'


