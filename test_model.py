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
        assert False
