

class Contact:
	"""
	Contact class

	Attributes:
		_thread_map (dict): map of user ID to slack contact thread
	"""
	_thread_map = dict()

	def __init__(self) -> None:
		pass

	def register(self, user_id, thread_ts):
		self._set_thread(user_id, thread_ts)

	def _set_thread(self, user_id, thread_ts):
		self._thread_map[user_id] = thread_ts

	def get_thread(self, user_id):
		return self._thread_map.get(user_id)