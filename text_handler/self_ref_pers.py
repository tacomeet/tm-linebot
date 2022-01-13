from linebot.models import TextSendMessage

import line
import message as ms
import slack


def self_ref_pers(line_bot_api, user, event):
    text = event.message.text
    ss_stage = user.get_session_stage()
    user.set_answer_msg(text)
    if ss_stage == 3:
        if text == 'Yes':
            slack.send_msg_to_other_thread(user.get_question_msg(), user.get_answer_msg(), user.get_thread_ts_other())
            user.reset_answer_msg()
            user.set_session_stage(5)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.self_ref.PERS_3_YES))
            user.set_question_msg(ms.self_ref.PERS_3_YES)
        elif text == 'No':
            slack.send_msg_to_other_thread(user.get_question_msg(), user.get_answer_msg(), user.get_thread_ts_other())
            user.reset_answer_msg()
            user.set_session_stage(4)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.self_ref.PERS_3_NO))
            line_bot_api.push_message(user.get_id(), TextSendMessage(text=ms.self_ref.PERS_3_NO_EX))
            user.set_question_msg(ms.self_ref.PERS_3_NO + '\n' + ms.self_ref.PERS_3_NO_EX)
    elif ss_stage == 7:
        if text == 'Yes':
            slack.send_msg_to_other_thread(user.get_question_msg(), user.get_answer_msg(), user.get_thread_ts_other())
            user.reset_answer_msg()
            user.set_session_stage(8)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.self_ref.PERS_7_YES))
            user.set_question_msg(ms.self_ref.PERS_7_YES)
        elif text == 'No':
            slack.send_msg_to_other_thread(user.get_question_msg(), user.get_answer_msg(), user.get_thread_ts_other())
            user.reset_answer_msg()
            user.set_session_stage(8)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.self_ref.PERS_7_NO))
            user.set_question_msg(ms.self_ref.PERS_7_NO)
    elif text == ms.default.KEY_NEXT:
        slack.send_msg_to_other_thread(user.get_question_msg(), user.get_answer_msg(), user.get_thread_ts_other())
        user.reset_answer_msg()
        msg = _route_next(user)
        if msg:
            line.reply_msg(line_bot_api, event, msg)


def _route_next(user):
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
        if ss_stage in (2, 6):
            user.set_question_msg(msg.alt_text)
        else:
            user.set_question_msg(msg)
        user.increment_session_stage()
        return msg
    if ss_stage == 8:
        slack.send_msg_to_other_thread(ms.default.END, None, user.get_thread_ts_other())
        user.reset()
        return ms.default.END
