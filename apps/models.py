from apps import db, lm
from flask.ext.login import  UserMixin
from sqlalchemy import (MetaData, Table, Column, Integer, String)
import sys
from hashlib import md5


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    method = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    password = db.Column(db.String(120), index=False, unique=False)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


def load_user_by_email_method(mail, met):
    return User.query.filter_by(email=mail, method=met).first()

class Post(db.Model):
    id = Column(db.Integer, primary_key = True)
    body = Column(db.String(140))
    timestamp = Column(db.DateTime)
    user_id = Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = Column(db.String(400))
    image = Column(db.String(400))
    rank = Column(db.Integer)
    title = Column(db.String(200))
    tags = Column(db.String(400))
    desc = Column(db.String(400))
    interval = Column(db.String(20))
