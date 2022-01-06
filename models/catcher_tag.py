from database.database import db


class CatcherTag(db.Model):
    __tablename__ = 'catcher_tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    catcher_id = db.Column(db.Integer())
    tag_id = db.Column(db.Integer())

    def __init__(self, catcher_id, tag_id):
        self.catcher_id = catcher_id
        self.tag_id = tag_id
