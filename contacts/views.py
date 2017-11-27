import pprint

from flask import *

from .auth import facebook, login_required

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html.j2')

@views.route('/contact/<contact_id>')
@login_required
def show_contact(contact_id):
    return render_template('contact-show.html.j2', contact_id=contact_id)

@views.route('/contacts')
def list():
    tags = request.get('tags')
    return pprint.pformat(tags)

