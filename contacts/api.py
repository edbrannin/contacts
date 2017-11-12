import pprint

from flask import *

from .auth import facebook, login_required
from .model import *

api = Blueprint('api', __name__)

@api.route('/tags')
@login_required
def all_tags():
    answer = [
            dict(
                href=url_for('api.show_tag', tag_id=tag.id),
                **tag.as_dict()
                )
            for tag in Tag.query.all()
            ]
    return jsonify(answer)

@api.route('/tags/<tag_id>')
@login_required
def show_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()
    people = tag.taggables
    people = [person.as_dict() for person in people]
    return jsonify(dict(tag=tag.as_dict(), people=people))

@api.route('/contacts')
@login_required
def list_contacts():
    tags = request.args.getlist('tag')
    answer = [
            contact.as_dict()
            for contact in Contact.list(*tags)
            ]
    return jsonify(answer)

@api.route('/contacts/<contact_id>')
@login_required
def get_contact(contact_id):
    contact = Contact.get_by_id(contact_id)
    answer = contact.as_dict()

    return jsonify(answer)

