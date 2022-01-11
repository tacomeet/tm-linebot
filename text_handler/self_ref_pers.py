from linebot.models import TextSendMessage

import line
import message as ms


def self_ref_pers(line_bot_api, user, event):
    text = event.message.text
    ss_stage = user.get_session_stage()
    if ss_stage == 3:
        if text == 'Yes':
            user.set_session_stage(5)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.self_ref.PERS_3_YES))
        elif text == 'No':
            user.set_session_stage(4)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.self_ref.PERS_3_NO))
            line_bot_api.push_message(user.get_id(), TextSendMessage(text=ms.self_ref.PERS_3_NO_EX))
    elif ss_stage == 7:
        if text == 'Yes':
            user.set_session_stage(8)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.self_ref.PERS_7_YES))
        elif text == 'No':
            user.set_session_stage(8)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.self_ref.PERS_7_NO))
    else:
        msg = route_next_self_ref_pers(user)
        if msg:
            line.reply_msg(line_bot_api, event, msg)


def route_next_self_ref_pers(user):
    ss_stage = user.get_session_stage()
    msg = None
    if ss_stage == 2:
        msg = ms.self_ref.PERS_2
    elif ss_stage == 4:
        msg = ms.self_ref.PERS_4
    elif ss_stage == 5:
        msg = ms.self_ref.PERS_5
    elif ss_stage == 6:
        msg = ms.self_ref.PERS_6
    if msg:
        user.increment_session_stage()
        return msg
    if ss_stage == 8:
        user.reset()
        return ms.default.END
