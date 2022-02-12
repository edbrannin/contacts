import pprint
from urllib.parse import urlparse, parse_qs
from datetime import datetime

import pytest
from flask import Flask, json
from faker import Faker

from contacts.model import *
from contacts import app as APP

fake = Faker()

TEST_EMAIL="test_user@example.com"

def fake_contacts(count):
    return [fake_contact() for c in range(count)]

def assert_contacts_equal(expected_contact, observed_contact):
    assert expected_contact.id == observed_contact.id
    assert expected_contact.name == observed_contact.name
    assert expected_contact.last_name == observed_contact.last_name
    assert expected_contact.address == observed_contact.address
    assert expected_contact.zip_code == observed_contact.zip_code
    assert expected_contact.home_phone == observed_contact.home_phone
    assert expected_contact.work_phone == observed_contact.work_phone
    assert expected_contact.email == observed_contact.email
    assert expected_contact.active == observed_contact.active
    assert expected_contact.verified_on == observed_contact.verified_on
    assert expected_contact.added_on == observed_contact.added_on
    assert expected_contact.note == observed_contact.note
    assert expected_contact.created_at == observed_contact.created_at
    assert expected_contact.updated_at == observed_contact.updated_at
    assert expected_contact.cached_tag_list == observed_contact.cached_tag_list
    assert expected_contact.mobile_phone == observed_contact.mobile_phone


def fake_contact():
    c = Contact()
    c.name = fake.name()
    c.last_name = c.name.split(' ')[-1]
    c.address = fake.address()
    c.zip_code = fake.zipcode()
    c.home_phone = fake.phone_number()
    c.work_phone = fake.phone_number()
    c.email = fake.safe_email()
    c.active = True
    c.verified_on = fake.past_date(start_date="-30d")
    c.added_on = fake.past_date(start_date=c.verified_on)
    c.note = fake.text()
    c.created_at = c.added_on
    c.updated_at = c.verified_on
    # TODO Tags fake.random_sample_unique(TEST_TAGS)
    # c.cached_tag_list = db.Column(db.Text)
    for tag in fake.random_sample_unique(TEST_TAGS[5:], length=3):
        c.add_tag(tag)
    # ALWAYS have TEST_TAGS[0] attached
    c.add_tag(TEST_TAGS[0])
    c.mobile_phone = "555-555-632"
    db.session.add(c)
    return c

TEST_TAGS = list(set(
    [fake.color_name() for x in range(25)]
    ))

@pytest.fixture
def app(autorun=True, scope="module"):
    # pass in test configuration
    if not APP.testing:
        APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        APP.config['DEBUG_TB_ENABLED'] = False
        APP.config['ALLOWED_USERS'] = TEST_EMAIL
        APP.testing = True
        db.init_app(APP)
    return APP


@pytest.fixture
def test_client(app, autorun=True, scope="module"):
    return app.test_client()



@pytest.fixture(autouse=True)
def db_tables(app):
    db.create_all()
    try:
        yield
    finally:
        db.session.remove()
        db.drop_all()

def login(test_client, name='Test User'):
    with test_client.session_transaction() as session:
        session['me'] = dict(email=TEST_EMAIL)


def test_list_tags_1_contact(test_client):
    c = fake_contact()
    db.session.commit()

    expected_tag_names = [t.name for t in c.tags]

    login(test_client)

    rv = test_client.get('/api/tags')
    observed_tag_names = [tag['name'] for tag in rv.json]
    assert set(expected_tag_names) == set(observed_tag_names)
    assert sorted(expected_tag_names) == sorted(observed_tag_names)

    pprint.pprint(rv.json)
    return
    # TODO Also assert this
    for tag in rv.json:
        assert tag.count == 1



def should_redirect_to_login(rv, path):
    assert rv.status_code == 302
    assert 'location' in rv.headers
    parsed_url = urlparse(rv.headers['location'])
    assert parsed_url.path == '/login'
    next_url = urlparse(parse_qs(parsed_url.query)['next'][0])
    assert next_url.path == path



def test_list_tags_login_required_redirect(test_client):
    rv = test_client.get('/api/tags')
    should_redirect_to_login(rv, '/api/tags')


def test_list_tags_login_required_success(test_client):
    login(test_client)

    rv = test_client.get('/api/tags')
    assert rv.status_code == 200
    # No tags defined yet
    assert rv.json == []

@pytest.mark.skip("TODO Implement")
def test_get_contacts_tagged(test_client):
    login(test_client)
    c = fake_contact()
    db.session.commit()

    # rv = test_client.get('/api/contacts/{}'.format(c.id))

def test_get_contact_need_login(test_client):
    c = fake_contact()
    db.session.commit()

    rv = test_client.get('/api/contacts/{}'.format(c.id))
    assert rv.status_code == 302
    assert 'location' in rv.headers
    parsed_url = urlparse(rv.headers['location'])
    assert parsed_url.path == '/login'
    next_url = urlparse(parse_qs(parsed_url.query)['next'][0])
    assert next_url.path == '/api/contacts/{}'.format(c.id)


def test_get_contact(test_client):
    login(test_client)

    c = fake_contact()
    db.session.commit()

    rv = test_client.get('/api/contacts/{}'.format(c.id))
    assert rv.json['id'] == c.id
    assert rv.json['name'] == c.name
    assert rv.json['last_name'] == c.last_name
    assert rv.json['address'] == c.address
    assert rv.json['zip_code'] == c.zip_code
    assert rv.json['home_phone'] == c.home_phone
    assert rv.json['work_phone'] == c.work_phone
    assert rv.json['email'] == c.email
    assert rv.json['active'] == c.active
    # assert rv.json['verified_on'] == c.verified_on
    # assert rv.json['added_on'] == c.added_on
    assert rv.json['note'] == c.note
    # assert rv.json['created_at'] == c.created_at
    # assert rv.json['updated_at'] == c.updated_at
    assert rv.json['cached_tag_list'] == c.cached_tag_list
    assert rv.json['tags'] == c.tag_names
    assert rv.json['mobile_phone'] == c.mobile_phone

def test_new_contact_needs_login(test_client):
    pass
    # TODO

def test_new_contact(test_client):
    login(test_client)

    assert Edit.query.count() == 0

    data = dict(
            tags=TEST_TAGS[0:3],
            name = 'Dalinar Kholin',
            last_name = 'Kholin',
            address = 'Urithru',
            zip_code = '11111',
            # home_phone = u'',
            # work_phone = u'',
            # mobile_phone = u'',
            email = 'blackthorn@alekhar.gov',
            active = True,
            # verified_on = db.Column(db.Date),
            # added_on = db.Column(db.Date),
            note = 'Highking of Alekhar',
            # created_at = db.Column(db.DateTime, default=datetime.datetime.now),
            # updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now),
            # cached_tag_list = u'',
            )

    # Make sure Contact.as_dict() handles tags
    assert TEST_TAGS[0] in data['tags']
    assert TEST_TAGS[1] in data['tags']
    assert TEST_TAGS[2] in data['tags']
    assert TEST_TAGS[3] not in data['tags']
    assert TEST_TAGS[4] not in data['tags']

    # Make sure String props have an expected class (to expose root cause for test errors)
    assert isinstance(data['name'], str), "{} = {} is a {}".format('name', data['name'], data['name'].__class__)

    rv = test_client.post('/api/contacts/', data=json.dumps(data), content_type="application/json")

    assert Edit.query.count() == 1
    assert rv.status_code == 200
    for k, v in list(rv.json.items()):
        if k in data and isinstance(data[k], str):
            assert data[k] == v, "Mismatch on {}".format(k)
    assert rv.json['created_at'] is not None
    assert rv.json['updated_at'] is not None

    # Make sure Contact.as_dict() handles tags
    assert TEST_TAGS[0] in rv.json['tags']
    assert TEST_TAGS[1] in rv.json['tags']
    assert TEST_TAGS[2] in rv.json['tags']
    assert TEST_TAGS[3] not in rv.json['tags']
    assert TEST_TAGS[4] not in rv.json['tags']

    new_contact_id = rv.json['id']

    # FIXME Ask just for the newest Edit; this only works because there's only 1 in the empty test DB
    edit = Edit.query.first()
    assert edit.user == TEST_EMAIL
    assert edit.subject_id == new_contact_id
    assert edit.subject_type == "Contact"
    assert edit.before is not None
    assert edit.after is not None
    assert edit.created_at is not None

    # Make sure a new request also returns the right thing
    rv = test_client.get('/api/contacts/{}'.format(new_contact_id))

    assert rv.status_code == 200
    for k, v in list(rv.json.items()):
        if k in data and isinstance(data[k], str):
            assert data[k] == v, "Mismatch on {}".format(k)
        elif k in data:
            print("TODO: Compare dates: data[{}] == {} ==? {}".format(k, data[k], v))

    # Make sure tags work
    assert TEST_TAGS[0] in rv.json['tags']
    assert TEST_TAGS[1] in rv.json['tags']
    assert TEST_TAGS[2] in rv.json['tags']
    assert TEST_TAGS[3] not in rv.json['tags']
    assert TEST_TAGS[4] not in rv.json['tags']


def test_put_contact(test_client):
    login(test_client)
    c = fake_contact()
    db.session.commit()

    assert  Edit.query.count() == 0

    data = c.as_dict(tags=True)

    # Make sure Contact.as_dict() handles tags
    assert TEST_TAGS[0] in data['tags']
    assert TEST_TAGS[1] not in data['tags']


    # Make sure String props have an expected class (to expose root cause for test errors)
    assert isinstance(data['name'], str), "{} = {} is a {}".format('name', data['name'], data['name'].__class__)
    # Mangle contact data
    for k, v in list(data.items()):
        if isinstance(v, str):
            print("************************")
            data[k] = "BOB " + v
    data['tags'].remove(TEST_TAGS[0])
    data['tags'].append(TEST_TAGS[1])
    assert TEST_TAGS[0] not in data['tags']
    assert TEST_TAGS[1] in data['tags']

    # Make sure the PUT response has the updated values
    rv = test_client.put('/api/contacts/{}'.format(c.id), data=json.dumps(data), content_type="application/json")

    assert Edit.query.count() == 1
    assert rv.status_code == 200
    for k, v in list(rv.json.items()):
        if isinstance(data[k], str):
            assert data[k] == v
        else:
            print("TODO: Compare dates: data[{}] == {} ==? {}".format(k, data[k], v))
    assert TEST_TAGS[0] not in rv.json['tags']
    assert TEST_TAGS[1] in rv.json['tags']

    # FIXME Ask just for the newest Edit; this only works because there's only 1 in the empty test DB
    edit = Edit.query.first()
    assert edit.user == TEST_EMAIL
    assert edit.subject_id == c.id
    assert edit.subject_type == "Contact"
    assert edit.before is not None
    assert edit.after is not None
    assert edit.created_at is not None

    # Make sure a new request also returns the right thing
    rv = test_client.get('/api/contacts/{}'.format(c.id))

    assert rv.status_code == 200
    for k, v in list(rv.json.items()):
        if isinstance(data[k], str):
            assert data[k] == v
        else:
            print("TODO: Compare dates: data[{}] == {} ==? {}".format(k, data[k], v))
    assert TEST_TAGS[0] not in rv.json['tags']
    assert TEST_TAGS[1] in rv.json['tags']

def test_put_contact_need_login(test_client):
    c = fake_contact()
    db.session.commit()

    url = '/api/contacts/{}'.format(c.id)
    rv = test_client.put(url, data=c.as_dict())
    should_redirect_to_login(rv, url)
    # should_redirect_to_login(rv, '/api/tags', data=c.as_dict())
