from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    status = db.Column(db.Integer())
    thread_ts = db.Column(db.String())
    follow = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime(), default=datetime.now)
