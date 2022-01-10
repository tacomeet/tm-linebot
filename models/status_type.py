from enum import auto, IntFlag


class StatusType(IntFlag):
    _BN_CREATE_TRACK1 = auto()
    _BN_CREATE_TRACK2 = auto()
    _BN_CREATE_TRACK3 = auto()
    _BN_CREATE_TRACK5 = auto()

    BN_CREATE = auto()
    BN_CREATE_TRACK1 = BN_CREATE | _BN_CREATE_TRACK1
    BN_CREATE_TRACK2 = BN_CREATE | _BN_CREATE_TRACK2
    BN_CREATE_TRACK3 = BN_CREATE | _BN_CREATE_TRACK3
    BN_CREATE_TRACK5 = BN_CREATE | _BN_CREATE_TRACK5

    _SELF_REF_EXP = auto()
    _SELF_REF_PERS = auto()
    _SELF_REF_VIS = auto()
    _SELF_REF_TURN = auto()

    SELF_REF = auto()
    SELF_REF_EXP = SELF_REF | _SELF_REF_EXP
    SELF_REF_PERS = SELF_REF | _SELF_REF_PERS
    SELF_REF_VIS = SELF_REF | _SELF_REF_VIS
    SELF_REF_TURN = SELF_REF | _SELF_REF_TURN

    CATCH_REC = auto()
    CONTACT = auto()


def is_included(parent: StatusType, child: StatusType) -> bool:
    return parent & child == parent
