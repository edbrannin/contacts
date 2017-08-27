from flask import Flask
from flask_testing import TestCase

from model import *

from faker import Faker
fake = Faker()

def fake_contacts(count):
    return [fake_contact() for c in range(count)]

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
    # c.cached_tag_list = db.Column(db.Text)
    c.mobile_phone = "555-555-632"
    return c

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

        assert cc.id == c.id
        assert cc.name == c.name
        assert cc.last_name == c.last_name
        assert cc.address == c.address
        assert cc.zip_code == c.zip_code
        assert cc.home_phone == c.home_phone
        assert cc.work_phone == c.work_phone
        assert cc.email == c.email
        assert cc.active == c.active
        assert cc.verified_on == c.verified_on
        assert cc.added_on == c.added_on
        assert cc.note == c.note
        assert cc.created_at == c.created_at
        assert cc.updated_at == c.updated_at
        assert cc.cached_tag_list == c.cached_tag_list
        assert cc.mobile_phone == c.mobile_phone



    def __repr__(self):
        return '<Contact %r>' % self.name

    def list(*tags):
        pass
