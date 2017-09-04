import pprint

from flask import *
from flask_login import LoginManager

from . import app
from .auth import facebook

@app.route('/')
def home():
    return render_template('home.html.j2')

def list(*tags):
    return pprint.pformat(Tags)
