from database.database import db


class Contact(db.Model):
	"""
	Contact class

	Attributes:
		_thread_map (dict): map of user ID to slack contact thread
	"""

	__tablename__ = 'contacts'

	ts = db.Column(db.String(), primary_key=True)
	user_id = db.Column(db.String())

	def __init__(self, ts, user_id) -> None:
		self.ts = ts
		self.user_id = user_id

	# def __init__(self) -> None:
	# 	self._thread_map = dict()
	# 	self._user_id_map = dict()

	# def register(self, user_id, thread_ts):
	# 	self._set_thread(user_id, thread_ts)
	# 	self._set_user(user_id, thread_ts)

	# def _set_thread(self, user_id, thread_ts):
	# 	self._thread_map[user_id] = thread_ts

	# def _set_user(self, user_id, thread_ts):
	# 	self._user_id_map[thread_ts] = user_id

	# def get_thread(self, user_id):
	# 	return self._thread_map.get(user_id)

	# def get_user(self, thread_ts):
	# 	return self._user_id_map.get(thread_ts)

def register(user_id: str, ts: str):
	con = Contact(ts=ts, user_id=user_id)
	db.session.add(con)
	db.session.commit()

def get_thread(user_id):
	thread_ts = Contact.query.filter_by(user_id=user_id).first()
	return thread_ts

def get_user(thread_ts):
	user_id = db.session.query(Contact).filter_by(ts=thread_ts).first()
	return user_id
