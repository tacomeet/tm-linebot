from enum import Enum, auto


class Status:
    """
    Status class

    Attributes:
        context (str): stage of the particular user
        type (Type): type of the status
    """

    def __init__(self):
        self.context = 0
        self.type = None

    def get_context(self):
        return self.context

    def set_context(self, context):
        self.context = context

    def get_type(self):
        return self.type

    def set_type(self, status_type):
        self.type = status_type


class Type(Enum):
    BN_CREATE = auto()
    BN_CREATE_TRACK1 = auto()
    BN_CREATE_TRACK2 = auto()
    BN_CREATE_TRACK3 = auto()
    BN_CREATE_TRACK5 = auto()
    SELF_REF = auto()
    CATCH_REC = auto()
