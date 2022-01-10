import slack
from linebot.models import TextSendMessage
import const.message as ms
import catcher_rec as cr
from database.database import db
from models.status_type import StatusType


def stage0(line_bot_api, user, event):
    text = event.message.text
    user_id = event.source.user_id
    if text == ms.KEY_SELF_REF:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_SELF_REF))
        line_bot_api.push_message(user_id, ms.MSG_SELF_REF_1)
        slack.start_self_rec(user.get_name())
        user.set_session_stage(2)
        user.set_session_type(StatusType.SELF_REF)
    elif text == ms.KEY_BN_CREATE:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_BN_CREATE))
        line_bot_api.push_message(user_id, TextSendMessage(text=ms.MSG_BN_CREATE_1))
        slack.start_bn_creation(user.get_name())
        user.set_session_stage(2)
        user.set_session_type(StatusType.BN_CREATE)
    elif text == ms.KEY_CATCHER:
        # execute cron job
        # schedule.run_pending()
        cr.refresh_catcher_tag()

        cr.register(user_id)
        slack.start_catcher_rec(user.get_name())

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_CATCHER))

        msg = ms.MSG_CATCHER_CONFIRM
        tag_id, question = cr.get_question(user_id)
        user.set_last_question_id(tag_id)
        user.set_is_matched(False)

        msg.alt_text = question
        msg.template.text = question
        line_bot_api.push_message(user_id, msg)

        user.set_session_type(StatusType.CATCH_REC)
        user.set_session_stage(1)
    elif text == ms.KEY_CONTACT:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_CONTACT_DEFAULT))
        user.set_session_stage(1)
        user.set_session_type(StatusType.CONTACT)
        res = slack.start_contact(user.get_name())
        user.set_thread_ts(res['message']['ts'])
        db.session.add(user)
    else:
        line_bot_api.reply_message(event.reply_token, ms.MSG_DEFAULT)
