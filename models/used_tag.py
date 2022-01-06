from database.database import db


class UsedTag(db.Model):
    __tablename__ = 'used_tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String())
    tag_id = db.Column(db.Integer())

    def __init__(self, user_id, tag_id):
        self.user_id = user_id
        self.tag_id = tag_id
