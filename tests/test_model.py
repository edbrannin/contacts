import time

import pytest
from flask import Flask
from faker import Faker

from contacts.model import *

fake = Faker()

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
    for tag in fake.random_sample_unique(TEST_TAGS, length=3):
        c.add_tag(tag)
    c.mobile_phone = "555-555-632"
    db.session.add(c)
    return c

TEST_TAGS = list(set(
    [fake.color_name() for x in range(25)]
    ))


@pytest.fixture
def app(autorun=True, scope="module"):
    # pass in test configuration
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)
    return app

@pytest.fixture(autouse=True)
def db_tables(app):
    db.create_all()
    try:
        yield
    finally:
        db.session.remove()
        db.drop_all()

def test_update():
    c = fake_contact()
    db.session.add(c)
    db.session.commit()

    updated_at = c.updated_at

    time.sleep(0.1)

    cc = Contact.query.first()
    new_last_name = c.last_name + " KING UNDER THE MOUNTAIN"
    cc.last_name = new_last_name
    db.session.add(cc)
    db.session.commit()

    count = Contact.query.count()
    assert count == 1
    ccc = Contact.query.first()
    assert ccc.last_name == new_last_name
    assert ccc.created_at == c.created_at
    assert ccc.updated_at > updated_at

def test_insert():
    c = fake_contact()

    db.session.add(c)
    db.session.commit()

    cc = Contact.query.first()

    assert_contacts_equal(c, cc)

def test_list_no_tags():
    c = fake_contact()
    c2 = fake_contact()
    while c.zip_code == c2.zip_code:
        c2 = fake_contact()

    db.session.add(c)
    db.session.add(c2)
    db.session.commit()

    contacts = Contact.list()
    contacts_by_zip = { c.zip_code : c for c in contacts }

    assert_contacts_equal(c, contacts_by_zip[c.zip_code])
    assert_contacts_equal(c2, contacts_by_zip[c2.zip_code])

def test_tags():
    c = fake_contact()
    c2 = fake_contact()
    print c.name
    for tag in c.tags:
        print tag
    print c2.name
    for tag in c2.tags:
        print tag
    db.session.add(c)
    db.session.add(c2)
    db.session.commit()
    print "Loading contacts"
    for contact in Contact.list():
        print contact.name
        for tag in contact.tags:
            print tag

def test_select_one_tag():
    contacts = fake_contacts(5)
    c = contacts[0]
    c3 = contacts[1]
    c.add_tag("TEST1")
    c.add_tag("TEST3")
    c3.add_tag("TEST3")
    db.session.commit()

    test1 = Contact.list("TEST1")
    assert len(test1) == 1
    assert test1[0] == c

    test3 = Contact.list("TEST3")
    assert len(test3) == 2
    assert c in test3
    assert c3 in test3

def test_select_two_tags():
    contacts = fake_contacts(5)
    c = contacts[0]
    c3 = contacts[1]
    c.add_tag("TEST1")
    c.add_tag("TEST3")
    c3.add_tag("TEST3")
    contacts[2].add_tag("TEST2")
    contacts[1].add_tag("TEST2")
    db.session.commit()

    test23 = Contact.list("TEST2", "TEST3")
    assert len(test23) == 1
    assert test23[0] == c3

