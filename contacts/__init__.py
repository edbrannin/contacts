import json

from flask import *
# from authlib.integrations.flask_client import OAuth, OAuthError
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('contacts.default_config')
app.config.from_envvar('SIM_CONTACTS_SETTINGS', silent=True)
app.config.from_pyfile('config.py')


app.secret_key = app.config.get('SECRET_KEY', "DEV TESTING")
if app.secret_key == "DEV TESTING":
    print("WARNING: Set a secret key!!!")

# toolbar = DebugToolbarExtension(app)


from .views import views
from .api import api


app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(views, url_prefix="")

@app.before_first_request
def print_url_map():
    print("URL map:")
    for rule in app.url_map.iter_rules():
        print(rule)

@app.before_first_request
def prime_edits():
    from .model import db, Contact, Edit
    db.create_all()
    edit_count = Edit.query.count()
    print("Edit count: {}".format(edit_count))
    if edit_count == 0:
        print("LOADING EDIT BASELINE")
        for contact in Contact.query.all():
            edit = Edit(
                    subject_type='Contact',
                    subject_id=contact.id,
                    after=json.dumps(contact.as_dict(tags=True)),
                    user='SYSTEM'
                    )
            db.session.add(edit)
        rows = db.session.commit()
        print("SAVED {} rows".format(rows))
