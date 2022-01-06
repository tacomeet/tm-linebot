from database.database import db


class CatcherCandidate(db.Model):
    __tablename__ = 'catcher_candidates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String())
    catcher_id = db.Column(db.Integer())

    def __init__(self, user_id, catcher_id):
        self.user_id = user_id
        self.catcher_id = catcher_id
