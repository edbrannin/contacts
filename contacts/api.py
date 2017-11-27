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
            contact.as_dict(href=url_for('views.show_contact', contact_id=contact.id))
            for contact in Contact.list(*tags)
            ]
    return jsonify(answer)

@api.route('/contacts/<contact_id>')
@login_required
def get_contact(contact_id):
    contact = Contact.get_by_id(contact_id)
    answer = contact.as_dict()

    return jsonify(answer)

REQUIRED_FIELDS = [
    "name",
    "last_name",
    "active",
    "note",
]

@api.route('/contacts/<contact_id>', methods=['PUT'])
@login_required
def put_contact(contact_id):
    contact = Contact.get_by_id(contact_id)

    # Required fields
    for name in REQUIRED_FIELDS:
        if name not in request.form:
            # FIXME
            raise "Missing required field: {}".format(name)

    if request.form['name']:
        contact.name = request.form['name']
    else:
        del contact.name

    if request.form['last_name']:
        contact.last_name = request.form['last_name']
    else:
        del contact.last_name

    if request.form['address']:
        contact.address = request.form['address']
    else:
        del contact.address

    if request.form['zip_code']:
        contact.zip_code = request.form['zip_code']
    else:
        del contact.zip_code

    if request.form['home_phone']:
        contact.home_phone = request.form['home_phone']
    else:
        del contact.home_phone

    if request.form['work_phone']:
        contact.work_phone = request.form['work_phone']
    else:
        del contact.work_phone

    if request.form['email']:
        contact.email = request.form['email']
    else:
        del contact.email

    if request.form['active']:
        contact.active = request.form['active']
    else:
        del contact.active

    if request.form['verified_on']:
        # contact.verified_on = request.form['verified_on']
        pass
    else:
        del contact.verified_on

    if request.form['note']:
        contact.note = request.form['note']
    else:
        del contact.note

    # TODO Tags

    if request.form['mobile_phone']:
        contact.mobile_phone = request.form['mobile_phone']
    else:
        del contact.mobile_phone

    answer = contact.as_dict()

    return jsonify(answer)

