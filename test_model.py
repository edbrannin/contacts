from flask import Flask
from flask_testing import TestCase

from model import *

from faker import Faker
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
    return c

TEST_TAGS = list(set(
    [fake.color_name() for x in range(25)]
    ))

class ContactsTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        # pass in test configuration
        app = Flask(__name__)
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_insert(self):
        c = fake_contact()

        db.session.add(c)
        db.session.commit()

        cc = Contact.query.first()

        assert_contacts_equal(c, cc)

    def test_list_no_tags(self):
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

    def test_tags(self):
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


