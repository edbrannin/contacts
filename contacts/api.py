import pprint

from flask import *

from .auth import facebook, login_required
from .model import *

api = Blueprint('api', __name__)

@api.route('/tags')
@login_required
def all_tags():
    answer = [tag.as_dict() for tag in Tag.query.all()]
    return jsonify(answer)

@api.route('/')
def home():
    return render_template('home.html.j2')

@api.route('/tags/<tag_id>')
@login_required
def show_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()
    people = tag.taggables
    people = [person.as_dict() for person in people]
    return jsonify(dict(tag=tag.as_dict(), people=people))

@api.route('/contacts')
def list_contacts():
    tags = request.get('tags')
    return pprint.pformat(tags)

