import datetime

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import subqueryload
from flask_sqlalchemy import SQLAlchemy
from . import app

db = SQLAlchemy()

class AsDict(object):
   def as_dict(self, **other):
       other.update({c.name: getattr(self, c.name) for c in self.__table__.columns})
       return other


db.init_app(app)

class Tag(db.Model, AsDict):
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

    @classmethod
    def all(self):
        """docstring for all"""
        return Tag.query.order_by(Tag.name).all()

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

class Edit(db.Model, AsDict):
    __tablename__ = 'edits'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_type = db.Column(db.String(255))
    subject_id = db.Column(db.Integer)
    user = db.Column(db.String(255))
    before = db.Column(db.Text)
    after = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

class Contact(db.Model, AsDict):
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
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now)
    cached_tag_list = db.Column(db.Text)
    mobile_phone = db.Column(db.String(255))

    taggings = db.relationship("Tagging", cascade="all, delete-orphan",
            # backref='taggable',
            # secondaryjoin=Tagging.taggable_type=="Contact")
            )
    tags = association_proxy("taggings", "tag"
            #, creator=Tag.named
            )

    @property
    def tag_names(self):
        return [tag.name for tag in self.tags]

    def __repr__(self):
        return '<Contact %r>' % self.name

    @classmethod
    def list(cls, *tags):
        q = cls.query.order_by(Contact.last_name)
        # https://stackoverflow.com/a/26303412/25625
        for tag in tags:
            q = q.filter(Contact.tags.any(Tag.name == tag))
        return q.all()

    @classmethod
    def get_by_id(cls, id, with_tags=True):
        q = cls.query.filter(Contact.id == id)
        if with_tags:
            q = q.options(subqueryload(Contact.taggings))
        return q.one()

    def add_tag(self, tag_name):
        tag = Tag.named(tag_name)
        tagging = Tagging()
        tagging.taggable = self
        tagging.tag = tag
        # self.tags.append(tag)
        self.taggings.append(tagging)

    def as_dict(self, tags=False):
        answer = super(Contact, self).as_dict()
        if tags:
            answer['tags'] = self.tag_names
        return answer

    def remove_tag(self, tag_name):
        remove_taggings = []
        for tag in self.tags:
            if tag_name == tag.name:
                remove_taggings.append(tag)
        for tagging in remove_taggings:
            self.tags.remove(tagging)

# TODO Audo-create Edits before_commit
# http://docs.sqlalchemy.org/en/latest/orm/session_state_management.html#session-attributes
# http://docs.sqlalchemy.org/en/latest/orm/events.html#sqlalchemy.orm.events.SessionEvents.before_commit
