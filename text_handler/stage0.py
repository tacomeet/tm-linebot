import slack
from linebot.models import TextSendMessage
# import message.self_ref
# import message.bn_create
# import message.catcher_rec
# import message.contact
# import message.default
import message as ms
import catcher_rec as cr
from database.database import db
from models.status_type import StatusType


def stage0(line_bot_api, user, event):
    text = event.message.text
    user_id = event.source.user_id
    user.set_session_start_timestamp()
    if text == ms.self_ref.KEY:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.self_ref.START))
        line_bot_api.push_message(user_id, ms.self_ref.M_1)
        res = slack.start_self_rec(user.get_name())
        user.set_thread_ts_other(res['message']['ts'])
        user.set_question_msg(ms.self_ref.START + '\n' + ms.self_ref.TYPE_SELECT)
        user.set_session_stage(2)
        user.set_session_type(StatusType.SELF_REF)
    elif text == ms.bn_create.KEY:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.bn_create.START))
        line_bot_api.push_message(user_id, TextSendMessage(text=ms.bn_create.M_1))
        res = slack.start_bn_creation(user.get_name())
        user.set_thread_ts_other(res['message']['ts'])
        user.set_question_msg(ms.bn_create.START + '\n' + ms.bn_create.M_1)
        user.set_session_stage(2)
        user.set_session_type(StatusType.BN_CREATE)
    elif text == ms.catcher_rec.KEY:
        # execute cron job
        # schedule.run_pending()
        cr.refresh_catcher_tag()

        cr.register(user_id)
        res = slack.start_catcher_rec(user.get_name())
        user.set_thread_ts_other(res['message']['ts'])

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.catcher_rec.START))

        msg = ms.catcher_rec.CONFIRM
        tag_id, question = cr.get_question(user_id)
        user.set_last_question_id(tag_id)
        user.set_is_matched(False)

        msg.alt_text = question
        msg.template.text = question
        line_bot_api.push_message(user_id, msg)

        user.set_session_type(StatusType.CATCH_REC)
        user.set_session_stage(1)
    elif text == ms.contact.KEY:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.contact.START))
        user.set_session_stage(1)
        user.set_session_type(StatusType.CONTACT)
        res = slack.start_contact(user.get_name())
        user.set_thread_ts_contact(res['message']['ts'])
        db.session.add(user)
    else:
        line_bot_api.reply_message(event.reply_token, ms.default.MENU)
