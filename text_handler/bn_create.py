import line
from models import User
from models.status_type import StatusType
import message.bn_create


def bn_create(line_bot_api, user, event):
    ss_type = user.get_session_type()

    if ss_type == StatusType.BN_CREATE:
        _bn_create(line_bot_api, user, event)
    else:
        bn_create_track(line_bot_api, user, event)


def _bn_create(line_bot_api, user, event):
    text = event.message.text
    ss_stage = user.get_session_stage()

    if text == message.default.KEY_NEXT:
        user.increment_session_stage()
        if ss_stage == 2:
            line.reply_msg(line_bot_api, event, message.bn_create.M_2)
        elif ss_stage == 3:
            line.reply_msg(line_bot_api, event, message.bn_create.M_3)
    elif text in (message.bn_create.M_3_1, message.bn_create.M_3_2, message.bn_create.M_3_3, message.bn_create.M_3_5):
        user.set_session_stage(1)
        if text == message.bn_create.M_3_1:
            user.set_session_type(StatusType.BN_CREATE_TRACK1)
        elif text == message.bn_create.M_3_2:
            user.set_session_type(StatusType.BN_CREATE_TRACK2)
        elif text == message.bn_create.M_3_3:
            user.set_session_type(StatusType.BN_CREATE_TRACK3)
        elif text == message.bn_create.M_3_5:
            user.set_session_type(StatusType.BN_CREATE_TRACK5)
        msg = get_bn_create_msg(user)
        line.reply_msg(line_bot_api, event, msg)


def bn_create_track(line_bot_api, user, event):
    text = event.message.text
    if text == message.default.KEY_NEXT:
        user.increment_session_stage()
        msg = get_bn_create_msg(user)
        line.reply_msg(line_bot_api, event, msg)


def get_bn_create_msg(user: User):
    ss_stage = user.get_session_stage()
    ss_type = user.get_session_type()

    bn_dict = message.bn_create.type_dict[ss_type]
    if ss_stage in bn_dict:
        if bn_dict[ss_stage] == message.default.END:
            user.reset()
        return bn_dict[ss_stage]
