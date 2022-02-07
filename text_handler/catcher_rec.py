from linebot.models import TextSendMessage, FlexSendMessage
import message as ms
import catcher_rec as cr
from models import User
import slack
import line


def catcher_rec(line_bot_api, user, event):
    user_id = event.source.user_id
    text = event.message.text

    if text not in ['Yes', 'No']:
        return

    possible_to_match = True
    user.set_answer_msg(text)
    if user.get_is_matched():
        if text == 'Yes':
            slack.send_msg_to_other_thread(user)
            user.reset_answer_msg()
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.catcher_rec.END))
            user.set_question_msg(ms.catcher_rec.END)
            slack.send_msg_to_other_thread(user)
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
        user.set_question_msg(ms.catcher_rec.SORRY)
        slack.send_msg_to_other_thread(user)
        cr.reset(user_id)
        user.reset()
    else:
        slack.send_msg_to_other_thread(user)
        user.reset_answer_msg()
        user.last_question_id = tag_id
        user.set_is_matched(False)
        msg = ms.catcher_rec.CONFIRM
        msg.alt_text = question
        msg.template.text = question
        line_bot_api.reply_message(event.reply_token, msg)
        user.set_question_msg(question)


def send_rec(line_bot_api, user: User, event, catcher_id):
    user.set_last_question_id(catcher_id)
    user.set_is_matched(True)
    msg = ms.catcher_rec.CONFIRM
    msg.alt_text = ms.catcher_rec.CONFIRM_TEXT
    msg.template.text = ms.catcher_rec.CONFIRM_TEXT
    slack.send_msg_to_other_thread(user)
    catcher = ms.catcher_rec.get_catcher(catcher_id)

    catcher_tags = cr.get_catcher_tags(user.get_id(), catcher_id)
    catcher_tags_msg = ms.catcher_rec.get_catcher_tags_msg(catcher_tags)
    line.send_single_msg(line_bot_api, user.get_id(), catcher_tags_msg)

    line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="catcher profile",
                                                                  contents=catcher))
    line_bot_api.push_message(user.id, msg)
    user.reset_answer_msg()
    user.set_question_msg('```' + '\n'
                          + 'Name: ' + catcher.body.contents[0].text + '\n'
                          + 'Work: ' + catcher.body.contents[1].contents[0].contents[1].text + '\n'
                          + 'Job: ' + catcher.body.contents[1].contents[1].contents[1].text + '\n'
                          + catcher_tags_msg + '\n'
                          + '```' + '\n'
                          + ms.catcher_rec.CONFIRM_TEXT)
