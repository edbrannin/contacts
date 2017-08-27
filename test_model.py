from flask import Flask
from flask_testing import TestCase

from model import *

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
        print "TODO: Insert!"
        c = Contact(name="First")
        c.name = "First!"
        c.last_name = "Last"
        c.address = "Some house"
        c.zip_code = "12345"
        c.home_phone = "555-555-1234"
        c.work_phone = "555-555-5555"
        c.email = "name@host.com"
        c.active = True
        # c.verified_on = db.Column(db.Date)
        # c.added_on = db.Column(db.Date)
        c.note = "This is a note."
        # c.created_at = db.Column(db.DateTime)
        # c.updated_at = db.Column(db.DateTime)
        # c.cached_tag_list = db.Column(db.Text)
        c.mobile_phone = "555-555-632"

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
