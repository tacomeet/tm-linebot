from linebot.models import TextSendMessage

import line
from models import User
from models.status_type import StatusType
import message as ms
from text_handler.self_ref_exp import self_ref_exp
from text_handler.self_ref_pers import self_ref_pers
from text_handler.self_ref_vis import self_ref_vis
from text_handler.self_ref_turn import self_ref_turn
import slack


def self_ref(line_bot_api, user: User, event):
    ss_type = user.get_session_type()
    user.set_answer_msg(event.message.text)

    if ss_type == StatusType.SELF_REF_EXP:
        self_ref_exp(line_bot_api, user, event)
    elif ss_type == StatusType.SELF_REF_PERS:
        self_ref_pers(line_bot_api, user, event)
    elif ss_type == StatusType.SELF_REF_VIS:
        self_ref_vis(line_bot_api, user, event)
    elif ss_type == StatusType.SELF_REF_TURN:
        self_ref_turn(line_bot_api, user, event)
    else:
        _self_ref(line_bot_api, user, event)


def _self_ref(line_bot_api, user: User, event):
    text = event.message.text
    if text in (ms.self_ref.M_1_EXP, ms.self_ref.M_1_PERS, ms.self_ref.M_1_VIS, ms.self_ref.M_1_TURN):
        slack.send_msg_to_other_thread(user)
        user.reset_answer_msg()
    if text == ms.self_ref.M_1_EXP:
        user.set_session_type(StatusType.SELF_REF_EXP)
        user.set_session_stage(2)
        user.set_question_msg(ms.self_ref.EXP_1)
        line.reply_msg(line_bot_api, event, ms.self_ref.EXP_1)
    elif text == ms.self_ref.M_1_PERS:
        user.set_session_type(StatusType.SELF_REF_PERS)
        user.set_session_stage(2)
        user.set_question_msg(ms.self_ref.PERS_1)
        line.reply_msg(line_bot_api, event, ms.self_ref.PERS_1)
    elif text == ms.self_ref.M_1_VIS:
        user.set_session_type(StatusType.SELF_REF_VIS)
        user.set_session_stage(2)
        user.set_question_msg(ms.self_ref.VIS_1)
        line.reply_msg(line_bot_api, event, ms.self_ref.VIS_1)
    elif text == ms.self_ref.M_1_TURN:
        user.set_session_type(StatusType.SELF_REF_TURN)
        user.set_session_stage(2)
        user.set_question_msg(ms.self_ref.TURN_1)
        line.reply_msg(line_bot_api, event, ms.self_ref.TURN_1)
