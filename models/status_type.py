from enum import IntEnum, auto


class StatusType(IntEnum):
    BN_CREATE = auto()
    BN_CREATE_TRACK1 = auto()
    BN_CREATE_TRACK2 = auto()
    BN_CREATE_TRACK3 = auto()
    BN_CREATE_TRACK5 = auto()
    SELF_REF = auto()
    CATCH_REC = auto()
    CONTACT = auto()
