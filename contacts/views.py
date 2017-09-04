import pprint

from flask import *

from . import app
from .auth import facebook, login_required

@app.route('/')
def home():
    return render_template('home.html.j2')

@app.route('/secure')
@login_required
def home_secure():
    return render_template('home.html.j2')

@app.route('/contacts')
def list():
    tags = request.get('tags')
    return pprint.pformat(tags)

