from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    taggings = db.relationship("Tagging", cascade="all, delete-orphan",
            # backref='taggable',
            # #secondaryjoin=Tagging.c.taggable_type=="Contact")
            )
    taggables = association_proxy("taggings", "taggable")

    @classmethod
    def named(cls, name):
        if isinstance(name, Tag):
            # Sometimes we get a Tag instead of a String.  huh.
            return name
        tag = cls.query.filter_by(name=name).first()
        if not tag:
            tag = Tag(name=name)
        return tag

    def __str__(self):
        return "Tag<{}>".format(self.name)

class Tagging(db.Model):
    __tablename__ = "taggings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    taggable_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))
    taggable_type = db.Column(db.String(255), default="Contact")
    created_at = db.Column(db.DateTime)

    tag = db.relationship(Tag, lazy='joined')
    taggable = db.relationship("Contact", lazy='joined')

class Contact(db.Model):
    __tablename__ = "contacts"

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

    taggings = db.relationship("Tagging", cascade="all, delete-orphan",
            # backref='taggable',
            # secondaryjoin=Tagging.taggable_type=="Contact")
            )
    tags = association_proxy("taggings", "tag"
            #, creator=Tag.named
            )


    def __repr__(self):
        return '<Contact %r>' % self.name

    @classmethod
    def list(cls, *tags):
        q = cls.query
        for tag in tags:
            q = q.filter(Contact.tags.any(Tag.name == tag))
            break
        return q.all()

    def add_tag(self, tag_name):
        tag = Tag.named(tag_name)
        tagging = Tagging()
        tagging.taggable = self
        tagging.tag = tag
        # self.tags.append(tag)
        self.taggings.append(tagging)