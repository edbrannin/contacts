import pprint
import StringIO

from flask import *

from .auth import facebook, login_required
from .model import *
from .mailing_labels import make_labels

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

@api.route('/tags/<tag_id>.pdf')
@login_required
def mailing_labels_for_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()
    out_filename = tag.name + ".pdf"
    people = tag.taggables
    people = sorted(people, key=lambda p: (
        # p.zip_code,
        p.last_name,
        ))

    strIO = StringIO.StringIO()
    make_labels(people, strIO)
    strIO.seek(0)
    return send_file(strIO,
                     attachment_filename=out_filename,
                     as_attachment=True)

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
    answer = contact.as_dict(tags=True)
    return jsonify(answer)

REQUIRED_FIELDS = [
    "name",
    "last_name",
    # "active",
    # "note",
]

def request_value(body, name):
    if name in body and body[name]:
        return body[name]
    return None

@api.route('/contacts/', methods=['POST'])
@login_required
def new_contact():
    contact = Contact()

    print "Getting JSON from {}".format(request.get_data())
    body = request.get_json()


    print "Checking required fields"
    # Required fields
    for name in REQUIRED_FIELDS:
        if name not in body:
            # FIXME
            raise Exception("Missing required field: {}.  Request: {}".format(name, body))

    print "Saving Before-state"
    before = contact.as_dict(tags=True)

    print "STARTING UPDATES"

    contact.name = request_value(body, 'name')
    contact.last_name = request_value(body, 'last_name')
    contact.address = request_value(body, 'address')
    contact.zip_code = request_value(body, 'zip_code')
    contact.home_phone = request_value(body, 'home_phone')
    contact.work_phone = request_value(body, 'work_phone')
    contact.mobile_phone = request_value(body, 'mobile_phone')
    contact.email = request_value(body, 'email')
    contact.active = request_value(body, 'active')
    # contact.verified_on = request_value(body, 'verified_on')
    contact.note = request_value(body, 'note')

    if body['tags']:
        old_tags = set(contact.tag_names)
        new_tags = set(body['tags'])
        for removed_tag in old_tags.difference(new_tags):
            contact.remove_tag(removed_tag)
        for new_tag in new_tags.difference(old_tags):
            contact.add_tag(new_tag)
    else:
        contact.tags.clear()


    print "Saving..."
    db.session.add(contact)
    db.session.flush()

    after = contact.as_dict(tags=True)
    edit = Edit(
            subject_type='Contact',
            subject_id=contact.id,
            before=json.dumps(before),
            after=json.dumps(after),
            user=session['me']['email'].strip().lower()
            )

    db.session.add(edit)
    db.session.commit()
    print "SAVED"

    after = contact.as_dict(
            tags=True,
            href=url_for('views.show_contact', contact_id=contact.id)
            )
    return jsonify(after)

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
    before = contact.as_dict(tags=True)

    print "STARTING UPDATES"

    contact.name = request_value(body, 'name')
    contact.last_name = request_value(body, 'last_name')
    contact.address = request_value(body, 'address')
    contact.zip_code = request_value(body, 'zip_code')
    contact.home_phone = request_value(body, 'home_phone')
    contact.work_phone = request_value(body, 'work_phone')
    contact.mobile_phone = request_value(body, 'mobile_phone')
    contact.email = request_value(body, 'email')
    contact.active = request_value(body, 'active')
    # contact.verified_on = request_value(body, 'verified_on')
    contact.note = request_value(body, 'note')

    if body['tags']:
        old_tags = set(contact.tag_names)
        new_tags = set(body['tags'])
        for removed_tag in old_tags.difference(new_tags):
            contact.remove_tag(removed_tag)
        for new_tag in new_tags.difference(old_tags):
            contact.add_tag(new_tag)
    else:
        contact.tags.clear()

    if body['mobile_phone']:
        contact.mobile_phone = body['mobile_phone']
    else:
        contact.mobile_phone = None

    print "Saving..."
    db.session.add(contact)
    db.session.flush()
    db.session.refresh(contact)

    after = contact.as_dict(tags=True)
    edit = Edit(
            subject_type='Contact',
            subject_id=contact.id,
            before=json.dumps(before),
            after=json.dumps(after),
            user=session['me']['email'].strip().lower()
            )

    db.session.add(edit)
    db.session.commit()
    print "SAVED"

    return jsonify(after)
