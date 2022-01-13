from linebot.models import TextSendMessage

import message as ms
import line
import slack


def self_ref_vis(line_bot_api, user, event):
    text = event.message.text
    ss_stage = user.get_session_stage()
    if ss_stage == 3:
        slack.send_msg_to_other_thread(user.get_question_msg(), user.get_answer_msg(), user.get_thread_ts_other())
        user.reset_answer_msg()
        if text == 'Yes':
            user.set_session_stage(9)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.self_ref.VIS_3_YES))
            line_bot_api.push_message(user.get_id(), TextSendMessage(text=ms.default.ASK_FOR_NEXT))
            user.set_question_msg(ms.self_ref.VIS_3_YES + '\n' + ms.default.ASK_FOR_NEXT)
        elif text == 'No':
            user.set_session_stage(4)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.self_ref.VIS_3_NO))
            line_bot_api.push_message(user.get_id(), TextSendMessage(text=ms.default.ASK_FOR_NEXT))
            user.set_question_msg(ms.self_ref.VIS_3_NO + '\n' + ms.default.ASK_FOR_NEXT)
    if ss_stage == 10:
        slack.send_msg_to_other_thread(user.get_question_msg(), user.get_answer_msg(), user.get_thread_ts_other())
        user.reset_answer_msg()
        if text == 'Yes':
            user.set_session_stage(12)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.self_ref.VIS_10_YES))
            line_bot_api.push_message(user.get_id(), TextSendMessage(text=ms.default.ASK_FOR_NEXT))
            user.set_question_msg(ms.self_ref.VIS_10_YES + '\n' + ms.default.ASK_FOR_NEXT)
        elif text == 'No':
            user.set_session_stage(11)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.self_ref.VIS_10_NO))
            line_bot_api.push_message(user.get_id(), TextSendMessage(text=ms.default.ASK_FOR_NEXT))
            user.set_question_msg(ms.self_ref.VIS_10_NO + '\n' + ms.default.ASK_FOR_NEXT)
    elif text == ms.default.KEY_NEXT:
        slack.send_msg_to_other_thread(user.get_question_msg(), user.get_answer_msg(), user.get_thread_ts_other())
        user.reset_answer_msg()
        msg = _route_next(user)
        if msg:
            line.reply_msg(line_bot_api, event, msg)
            if ss_stage not in (2, 9, 12):
                line_bot_api.push_message(user.get_id(), TextSendMessage(text=ms.default.ASK_FOR_NEXT))


def _route_next(user):
    ss_stage = user.get_session_stage()
    msg = None
    if ss_stage == 2:
        msg = ms.self_ref.VIS_2
    elif ss_stage == 4:
        msg = ms.self_ref.VIS_4
    elif ss_stage == 5:
        msg = ms.self_ref.VIS_5
    elif ss_stage == 6:
        msg = ms.self_ref.VIS_6
    elif ss_stage == 7:
        msg = ms.self_ref.VIS_7
    elif ss_stage == 8:
        msg = ms.self_ref.VIS_8
    elif ss_stage == 9:
        msg = ms.self_ref.VIS_9
    elif ss_stage == 11:
        msg = ms.self_ref.VIS_11
    if msg:
        if ss_stage in (2, 9):
            user.set_question_msg(msg.alt_text)
        else:
            user.set_question_msg(msg)
        user.increment_session_stage()
        return msg
    if ss_stage == 12:
        slack.send_msg_to_other_thread(ms.default.END, None, user.get_thread_ts_other())
        user.reset()
        return ms.default.END
