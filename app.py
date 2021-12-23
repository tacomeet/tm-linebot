import logging
import os
import sys
import random

from flask import Flask, abort, request
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ConfirmTemplate, MessageAction, TemplateSendMessage, ButtonsTemplate,
    URIAction, PostbackAction, CarouselColumn, CarouselTemplate, ImageCarouselTemplate, ImageCarouselColumn,
    DatetimePickerAction, BubbleContainer, ImageComponent, BoxComponent, TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, FlexSendMessage, QuickReply, QuickReplyButton, CameraAction, CameraRollAction, LocationAction,
    SourceUser,
)
from werkzeug.middleware.proxy_fix import ProxyFix

import catcher
import config
import session as ss
import message as ms
import slack
import status as st
import contact

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

channel_access_token = config.LINE_CHANNEL_ACCESS_TOKEN
channel_secret = config.LINE_CHANNEL_SECRET
if channel_secret is None or channel_access_token is None:
    app.logger.error('Specify LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN in .env file')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

s = ss.Session()

cs = catcher.Catchers()

con = contact.Contact()

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        app.logger.error(f"Got exception from LINE Messaging API: {e.message}\n")
        for m in e.error.details:
            app.logger.error(f"  {m.property}: {m.message}")
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    user_id = event.source.user_id

    s.register(user_id)
    ctx = s.get_context(user_id)
    ss_type = s.get_type(user_id)

    # End
    if ctx != 0 and text == ms.KEY_END:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_END))
        s.reset(user_id)
    # Start
    elif ctx == 0 and text == ms.KEY_BN_CREATE:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_BN_CREATE))
        line_bot_api.push_message(user_id, TextSendMessage(text=ms.MSG_BN_CREATE_1))
        s.set_context(user_id, 2)
        s.set_type(user_id, st.Type.BN_CREATE)
    elif ctx == 0 and text == ms.KEY_CATCHER:
        cs.register(user_id)

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_CATCHER))
        msg = ms.MSG_CATCHER_CONFIRM
        tag, q = cs.get_question(user_id)
        msg.alt_text = q
        msg.template.text = q
        line_bot_api.push_message(user_id, msg)
        s.set_type(user_id, st.Type.CATCH_REC)
    # Yes or No
    elif ss_type == st.Type.CATCH_REC and text in ['Yes', 'No']:
        if text == 'Yes':
            cs.include_tag(user_id, cs.used_tags[user_id][-1])
        else:
            cs.exclude_tag(user_id, cs.used_tags[user_id][-1])
        if cs.is_determined(user_id):
            msg = ms.MSG_CATCHER_END
            rec = cs.cand_by_user[user_id][0]
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
            line_bot_api.push_message(user_id, FlexSendMessage(alt_text="hello", contents=ms.get_catcher(rec)))
            s.reset(user_id)
        else:
            tag, q = cs.get_question(user_id)
            if not tag:
                if len(cs.cand_by_user[user_id]) == 0:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_CATCHER_SORRY))
                else:
                    rec = random.choice(cs.cand_by_user[user_id])
                    msg = ms.MSG_CATCHER_END
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
                    line_bot_api.push_message(user_id, FlexSendMessage(alt_text="hello", contents=ms.get_catcher(rec)))
                s.reset(user_id)
            else:
                msg = ms.MSG_CATCHER_CONFIRM
                tag, q = cs.get_question(user_id)
                msg.alt_text = q
                msg.template.text = q
                line_bot_api.reply_message(event.reply_token, msg)

    # Slack contact
    elif ctx == 0 and text == ms.KEY_CONTACT:
        profile = line_bot_api.get_profile(user_id)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_CONTACT_DEFAULT))
        s.set_context(user_id, 1)
        s.set_type(user_id, st.Type.CONTACT)
        res = slack.start_contact(profile.display_name)
        con.register(user_id, res['message']['ts'])
    elif s.get_type(user_id) == st.Type.CONTACT:
        profile = line_bot_api.get_profile(user_id)
        # TODO: Processing at the end of contact
        if text == ms.KEY_END:
            print('End of cotact')
        else:
            slack.send_msg_to_thread(profile.display_name, text, con.get_thread(user_id))

    # Next
    elif text == '次':
        msg = route_next(user_id)
        if isinstance(msg, str):
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
        else:
            line_bot_api.reply_message(event.reply_token, msg)
    # Route in BN Create
    elif text in (ms.MSG_BN_CREATE_3_1, ms.MSG_BN_CREATE_3_2, ms.MSG_BN_CREATE_3_3, ms.MSG_BN_CREATE_3_5):
        s.set_context(user_id, 1)
        if text == ms.MSG_BN_CREATE_3_1:
            s.set_type(user_id, st.Type.BN_CREATE_TRACK1)
        elif text == ms.MSG_BN_CREATE_3_2:
            s.set_type(user_id, st.Type.BN_CREATE_TRACK2)
        elif text == ms.MSG_BN_CREATE_3_3:
            s.set_type(user_id, st.Type.BN_CREATE_TRACK3)
        elif text == ms.MSG_BN_CREATE_3_5:
            s.set_type(user_id, st.Type.BN_CREATE_TRACK5)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=route_bn_create(user_id)))

    else:
        if ctx == 0:
            line_bot_api.reply_message(event.reply_token, ms.MSG_DEFAULT)

    if text == 'debug':
        app.logger.info(s.get_type(user_id), s.get_context(user_id))


# Message-branch dictionary
bn_dict_1 = {1: ms.MSG_BN_CREATE_T1_1, 2: ms.MSG_BN_CREATE_T1_2, 3: ms.MSG_BN_CREATE_T1_3, 4: ms.MSG_END}
bn_dict_2 = {1: ms.MSG_BN_CREATE_T2_1, 2: ms.MSG_BN_CREATE_T2_2, 3: ms.MSG_BN_CREATE_T2_3, 4: ms.MSG_END}
bn_dict_3 = {1: ms.MSG_BN_CREATE_T3_1, 2: ms.MSG_BN_CREATE_T3_2, 3: ms.MSG_END}
bn_dict_4 = {1: ms.MSG_BN_CREATE_T5_1, 2: ms.MSG_BN_CREATE_T5_2, 3: ms.MSG_END}

type_dict = {st.Type.BN_CREATE_TRACK1: bn_dict_1,
             st.Type.BN_CREATE_TRACK2: bn_dict_2,
             st.Type.BN_CREATE_TRACK3: bn_dict_3,
             st.Type.BN_CREATE_TRACK5: bn_dict_4}


def route_bn_create(user_id: str):
    ss_type = s.get_type(user_id)
    ctx = s.get_context(user_id)
    s.increment_context(user_id)

    if ss_type in type_dict:
        bn_dict = type_dict[ss_type]

    if ctx in bn_dict:
        if bn_dict[ctx] == ms.MSG_END:
            s.reset(user_id)
        return bn_dict[ctx]


def route_next(user_id: str):
    ctx = s.get_context(user_id)
    ss_type = s.get_type(user_id)
    if ss_type == st.Type.BN_CREATE:
        s.increment_context(user_id)
        print(s.get_context(user_id))
        if ctx == 2:
            return ms.MSG_BN_CREATE_2
        elif ctx == 3:
            return ms.MSG_BN_CREATE_3
    elif ss_type in (
            st.Type.BN_CREATE_TRACK1, st.Type.BN_CREATE_TRACK2, st.Type.BN_CREATE_TRACK3, st.Type.BN_CREATE_TRACK5):
        return route_bn_create(user_id)


if __name__ == "__main__":
    # line_bot_api.push_message('U728af6e5de3a116a994649e896faa6d7', ))
    app.run(host="localhost", port=8000)
