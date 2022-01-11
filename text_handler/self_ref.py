from linebot.models import TextSendMessage

from models import User
from models.status_type import StatusType
import message as ms
from text_handler.self_ref_exp import self_ref_exp
from text_handler.self_ref_pers import self_ref_pers


def self_ref(line_bot_api, user: User, event):
    ss_type = user.get_session_type()

    if ss_type == StatusType.SELF_REF_EXP:
        self_ref_exp(line_bot_api, user, event)
    elif ss_type == StatusType.SELF_REF_PERS:
        self_ref_pers(line_bot_api, user, event)
    elif ss_type == StatusType.SELF_REF_VIS:
        pass
    elif ss_type == StatusType.SELF_REF_TURN:
        pass
    else:
        _self_ref(line_bot_api, user, event)


def _self_ref(line_bot_api, user: User, event):
    text = event.message.text
    if text == ms.self_ref.M_1_EXP:
        user.set_session_type(StatusType.SELF_REF_EXP)
        user.set_session_stage(2)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.self_ref.EXP_1))
        line_bot_api.push_message(user.get_id(), TextSendMessage(text=ms.self_ref.EXP_1_EX))
    elif text == ms.self_ref.M_1_PERS:
        user.set_session_type(StatusType.SELF_REF_PERS)
        user.set_session_stage(2)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.self_ref.PERS_1))
        line_bot_api.push_message(user.get_id(), TextSendMessage(text=ms.self_ref.PERS_1_EX))
    elif text == ms.self_ref.M_1_VIS:
        user.set_session_type(StatusType.SELF_REF_VIS)
        user.set_session_stage(2)
        pass
    elif text == ms.self_ref.M_1_TURN:
        user.set_session_type(StatusType.SELF_REF_TURN)
        user.set_session_stage(2)
        pass
