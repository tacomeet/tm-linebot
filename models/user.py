from datetime import datetime
from database.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    status = db.Column(db.Integer())
    thread_ts = db.Column(db.String())
    created_at = db.Column(db.DateTime(), default=datetime.now)

    def __init__(self, id, name, status=0, thread_ts=None):
        self.id = id
        self.name = name
        self.status = status
        self.thread_ts = thread_ts
