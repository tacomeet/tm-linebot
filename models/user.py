from datetime import datetime
from database.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    session_type = db.Column(db.Integer())
    session_stage = db.Column(db.Integer())
    thread_ts = db.Column(db.String())
    is_matched = db.Column(db.Boolean())
    last_question_id = db.Column(db.Integer())
    created_at = db.Column(db.DateTime(), default=datetime.now)

    def __init__(self, id, name, session_type=None, session_stage=0, thread_ts=None):
        self.id = id
        self.name = name
        self.session_type = session_type
        self.session_stage = session_stage
        self.thread_ts = thread_ts
        self.is_matched = False
        self.last_question_id = None

    def reset(self):
        self.session_type = None
        self.session_stage = 0

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_session_stage(self):
        return self.session_stage

    def set_session_stage(self, session_stage):
        self.session_stage = session_stage

    def get_session_type(self):
        return self.session_type

    def set_session_type(self, session_type):
        self.session_type = session_type

    def increment_session_stage(self):
        self.session_stage += 1

    def get_thread_ts(self):
        return self.thread_ts

    def set_thread_ts(self, thread_ts):
        self.thread_ts = thread_ts

    def get_is_matched(self):
        return self.is_matched

    def set_is_matched(self, is_matched):
        self.is_matched = is_matched

    def set_last_question_id(self, question_id):
        # question_id is either tag id or catcher id
        self.last_question_id = question_id
