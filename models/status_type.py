from enum import IntEnum


class StatusType(IntEnum):
    BN_CREATE = 1
    BN_CREATE_TRACK1 = 2
    BN_CREATE_TRACK2 = 3
    BN_CREATE_TRACK3 = 4
    BN_CREATE_TRACK5 = 5
    SELF_REF = 6
    SELF_REF_EXP = 7
    SELF_REF_PERS = 8
    SELF_REF_VIS = 9
    SELF_REF_TURN = 10
    CATCH_REC = 11
    CONTACT = 12
