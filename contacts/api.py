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
                people_href=url_for('api.list_contacts', tag=tag.name),
                **tag.as_dict()
                )
            for tag in Tag.all()
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
    tags = [t for t in tags if t]
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

    print "Getting JSON from {}".format(request.get_data())
    body = request.get_json()


    print "Checking required fields"
    # Required fields
    for name in REQUIRED_FIELDS:
        if name not in body:
            # FIXME
            raise Exception("Missing required field: {}.  Request: {}".format(name, body))

    print "Saving Before-state"
    before = contact.as_dict()

    print "STARTING UPDATES"

    if body['name']:
        contact.name = body['name']
    else:
        contact.name = None

    print "NAME DONE"
    if body['last_name']:
        contact.last_name = body['last_name']
    else:
        contact.last_name = None

    if body['address']:
        contact.address = body['address']
    else:
        contact.address = None

    if body['zip_code']:
        contact.zip_code = body['zip_code']
    else:
        contact.zip_code = None

    if body['home_phone']:
        contact.home_phone = body['home_phone']
    else:
        contact.home_phone = None

    if body['work_phone']:
        contact.work_phone = body['work_phone']
    else:
        contact.work_phone = None

    if body['email']:
        contact.email = body['email']
    else:
        contact.email = None

    if body['active']:
        contact.active = body['active']
    else:
        contact.active = None

    print "PROGRESSING"
    
    if body['verified_on']:
        # contact.verified_on = body['verified_on']
        pass
    else:
        contact.verified_on = None

    if body['note']:
        contact.note = body['note']
    else:
        contact.note = None

    # TODO Tags

    if body['mobile_phone']:
        contact.mobile_phone = body['mobile_phone']
    else:
        contact.mobile_phone = None

    after = contact.as_dict()
    edit = Edit(
            subject_type='Contact',
            subject_id=contact.id,
            before=json.dumps(before),
            after=json.dumps(after),
            user=session['me']['email'].strip().lower()
            )

    print "Saving..."
    db.session.add(contact)
    db.session.add(edit)
    db.session.commit()
    print "SAVED"


    return jsonify(after)
