from datetime import datetime
from database.database import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    status = db.Column(db.Integer())
    thread_ts = db.Column(db.String())
    follow = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime(), default=datetime.now)

    def __init__(self, id, ts):
        self.id = id
        self.thread_ts = ts

def register_thread(user_id: str, ts: str):
    con = db.session.query(User).filter_by(id=user_id).first()
    if con is None:
        con = User(user_id, ts)
    else:
        con.thread_ts = ts
    db.session.add(con)
    db.session.commit()

def get_thread_by_id(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    return user.thread_ts

def get_user_by_thread_ts(thread_ts):
    user = db.session.query(User).filter_by(thread_ts=thread_ts).first()
    return user.id