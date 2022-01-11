from linebot.models import TextSendMessage, FlexSendMessage
import message as ms
import catcher_rec as cr
from models import User


def catcher_rec(line_bot_api, user, event):
    user_id = event.source.user_id
    text = event.message.text

    if text not in ['Yes', 'No']:
        return

    possible_to_match = True
    if user.get_is_matched():
        if text == 'Yes':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.catcher_rec.END))
            cr.reset(user_id)
            user.reset()
            return
        else:
            cr.exclude_catcher(user_id, user.last_question_id)
    else:
        if text == 'No':
            cr.exclude_tag(user_id, user.last_question_id)
            possible_to_match = False
    if possible_to_match:
        catcher_id = cr.get_rec(user_id)
        if catcher_id is not None:
            send_rec(line_bot_api, user, event, catcher_id)
            return
    tag_id, question = cr.get_question(user_id)
    if not tag_id:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.catcher_rec.SORRY))
        cr.reset(user_id)
        user.reset()
    else:
        user.last_question_id = tag_id
        user.set_is_matched(False)
        msg = ms.catcher_rec.CONFIRM
        msg.alt_text = question
        msg.template.text = question
        line_bot_api.reply_message(event.reply_token, msg)


def send_rec(line_bot_api, user: User, event, catcher_id):
    user.set_last_question_id(catcher_id)
    user.set_is_matched(True)
    msg = ms.catcher_rec.CONFIRM
    msg.alt_text = ms.catcher_rec.CONFIRM_TEXT
    msg.template.text = ms.catcher_rec.CONFIRM_TEXT
    line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="catcher profile",
                                                                  contents=ms.catcher_rec.get_catcher(catcher_id)))
    line_bot_api.push_message(user.id, msg)
