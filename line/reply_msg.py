from linebot.models import TextSendMessage


def send_single_msg(line_bot_api, user_id, msg):
    if msg is None:
        return
    if isinstance(msg, str):
        line_bot_api.push_message(user_id, TextSendMessage(text=msg))
    else:
        line_bot_api.push_message(user_id, msg)


def reply_single_msg(line_bot_api, event, msg):
    if msg is None:
        return
    if isinstance(msg, str):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
    else:
        line_bot_api.reply_message(event.reply_token, msg)


def reply_msg(line_bot_api, event, msg):
    if msg is None:
        return
    if isinstance(msg, list):
        reply_single_msg(line_bot_api, event, msg[0])
        for m in msg[1:]:
            send_single_msg(line_bot_api, event.source.user_id, m)
    else:
        reply_single_msg(line_bot_api, event, msg)
