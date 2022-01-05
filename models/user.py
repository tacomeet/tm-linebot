from datetime import datetime
from database.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    session_type = db.Column(db.Integer())
    session_stage = db.Column(db.Integer())
    thread_ts = db.Column(db.String())
    created_at = db.Column(db.DateTime(), default=datetime.now)

    def __init__(self, id, name, session_type=None, session_stage=0, thread_ts=None):
        self.id = id
        self.name = name
        self.session_type = session_type
        self.session_stage = session_stage
        self.thread_ts = thread_ts

    def reset(self):
        self.session_type = None
        self.session_stage = 0

    def set_session_stage(self, session_stage):
        self.session_stage = session_stage

    def set_session_type(self, session_type):
        self.session_type = session_type

    def increment_session_stage(self):
        self.session_stage += 1
