import models.status as status


class Session:
    """
    Session class

    Attributes:
        _status_map (dict): map of user ID to Status instance

    """
    _status_map = dict()

    def register(self, user_id: str):
        if self._get_status(user_id) is None:
            self._set_status(user_id, status.Status())

    def reset(self, user_id: str):
        self._set_status(user_id, status.Status())

    def _get_status(self, user_id: str) -> status.Status:
        return self._status_map.get(user_id)

    def _set_status(self, user_id: str, status: status.Status):
        self._status_map[user_id] = status

    def get_context(self, user_id: str) -> str:
        return self._get_status(user_id).get_context()

    def get_type(self, user_id: str) -> status.Type:
        return self._get_status(user_id).get_type()

    def set_context(self, user_id: str, context):
        st = self._get_status(user_id)
        st.set_context(context)

    def set_type(self, user_id: str, status_type: status.Type):
        st = self._get_status(user_id)
        st.set_type(status_type)

    def increment_context(self, user_id: str):
        st = self._get_status(user_id)
        st.set_context(st.get_context() + 1)
