from linebot.models import TextSendMessage


def reply_msg(line_bot_api, event, msg):
    if isinstance(msg, str):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
    else:
        line_bot_api.reply_message(event.reply_token, msg)