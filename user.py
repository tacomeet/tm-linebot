from app import app_db


class User(app_db.Model):
    __tablename__ = 'users'
    id = app_db.Column(app_db.String(), primary_key=True)
    name = app_db.Column(app_db.String())
    status = app_db.Column(app_db.Integer())
    thread_ts = app_db.Column(app_db.String())
    follow = app_db.Column(app_db.Boolean())

    # created_at = app_db.Column(app_db.DateTime())
