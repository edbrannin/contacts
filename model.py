from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    last_name = db.Column(db.String(255), index=True)
    address = db.Column(db.Text)
    zip_code = db.Column(db.String(255), index=True)
    home_phone = db.Column(db.String(255))
    work_phone = db.Column(db.String(255))
    email = db.Column(db.String(255), index=True)
    active = db.Column(db.Boolean)
    verified_on = db.Column(db.Date)
    added_on = db.Column(db.Date)
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    cached_tag_list = db.Column(db.Text)
    mobile_phone = db.Column(db.String(255))

    def __repr__(self):
        return '<Contact %r>' % self.name

    def list(*tags):
        pass

