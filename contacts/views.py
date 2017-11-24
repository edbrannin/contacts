import pprint

from flask import *

from .auth import facebook, login_required

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html.j2')

@views.route('/secure')
@login_required
def home_secure():
    return render_template('home.html.j2')

@views.route('/contacts')
def list():
    tags = request.get('tags')
    return pprint.pformat(tags)

