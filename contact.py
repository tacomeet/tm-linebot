

class Contact:
	"""
	Contact class

	Attributes:
		_thread_map (dict): map of user ID to slack contact thread
	"""
	_thread_map = dict()
	_user_id_map = dict()

	def __init__(self) -> None:
		pass

	def register(self, user_id, thread_ts):
		self._set_thread(user_id, thread_ts)
		self._set_user(user_id, thread_ts)

	def _set_thread(self, user_id, thread_ts):
		self._thread_map[user_id] = thread_ts

	def _set_user(self, user_id, thread_ts):
		self._user_id_map[thread_ts] = user_id

	def get_thread(self, user_id):
		return self._thread_map.get(user_id)

	def get_user(self, thread_ts):
		return self._user_id_map.get(thread_ts)