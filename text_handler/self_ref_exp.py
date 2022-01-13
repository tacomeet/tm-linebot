from linebot.models import TextSendMessage

import message as ms
import line


def self_ref_exp(line_bot_api, user, event):
    text = event.message.text
    ss_stage = user.get_session_stage()
    if ss_stage == 3:
        if text == 'Yes':
            user.set_session_stage(5)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.self_ref.EXP_3_YES))
        elif text == 'No':
            user.set_session_stage(4)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.self_ref.EXP_3_NO))
    elif text == ms.default.KEY_NEXT:
        msg = _route_next(user)
        if msg:
            line.reply_msg(line_bot_api, event, msg)


def _route_next(user):
    ss_stage = user.get_session_stage()
    msg = None
    if ss_stage == 2:
        msg = ms.self_ref.EXP_2
    elif ss_stage == 4:
        msg = ms.self_ref.EXP_4
    elif ss_stage == 5:
        msg = ms.self_ref.EXP_5
    elif ss_stage == 6:
        msg = ms.self_ref.EXP_6
    elif ss_stage == 7:
        msg = ms.self_ref.EXP_7
    elif ss_stage == 8:
        msg = ms.self_ref.EXP_8
    elif ss_stage == 9:
        msg = ms.self_ref.EXP_9
    if msg:
        user.increment_session_stage()
        return msg
    if ss_stage == 10:
        user.reset()
        return ms.default.END
