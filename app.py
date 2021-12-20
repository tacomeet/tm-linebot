import logging
import os
import sys

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

import session as ss
import message as ms
import status as st

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
channel_secret = os.getenv('LINE_CHANNEL_SECRET')
if channel_secret is None or channel_access_token is None:
    app.logger.error('Specify LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN as environment variables.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

s = ss.Session()


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

    # End
    if ctx != 0 and text == ms.KEY_END:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_END))
        s.reset(user_id)
    # Start
    elif ctx == 0 and ms.KEY_BN_CREATE in text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_BN_CREATE))
        line_bot_api.push_message(user_id, TextSendMessage(text=ms.MSG_BN_CREATE_1))
        s.set_context(user_id, 2)
        s.set_type(user_id, st.Type.BN_CREATE)
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

    # Example
    elif text == 'confirm':
        confirm_template = ConfirmTemplate(text='Do it?', actions=[
            MessageAction(label='Yes', text='Yes!'),
            MessageAction(label='No', text='No!'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'buttons':
        buttons_template = ButtonsTemplate(
            title='My buttons sample', text='Hello, my buttons', actions=[
                URIAction(label='Go to line.me', uri='https://line.me'),
                PostbackAction(label='ping', data='ping'),
                PostbackAction(label='ping with text', data='ping', text='ping'),
                MessageAction(label='Translate Rice', text='米')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'image_carousel':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerAction(label='datetime',
                                                            data='datetime_postback',
                                                            mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerAction(label='date',
                                                            data='date_postback',
                                                            mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'quick_reply':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='Quick reply',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(label="label1", data="data1")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="label2", text="text2")
                        ),
                        QuickReplyButton(
                            action=DatetimePickerAction(label="label3",
                                                        data="data3",
                                                        mode="date")
                        ),
                        QuickReplyButton(
                            action=CameraAction(label="label4")
                        ),
                        QuickReplyButton(
                            action=CameraRollAction(label="label5")
                        ),
                        QuickReplyButton(
                            action=LocationAction(label="label6")
                        ),
                    ])))
    else:
        if ctx == 0:
            line_bot_api.reply_message(event.reply_token, ms.MSG_DEFAULT)

    if text == 'debug':
        app.logger.info(s.get_type(user_id), s.get_context(user_id))


def route_bn_create(user_id: str):
    ss_type = s.get_type(user_id)
    ctx = s.get_context(user_id)
    s.increment_context(user_id)
    if ss_type == st.Type.BN_CREATE_TRACK1:
        if ctx == 1:
            return ms.MSG_BN_CREATE_T1_1
        elif ctx == 2:
            return ms.MSG_BN_CREATE_T1_2
        elif ctx == 3:
            return ms.MSG_BN_CREATE_T1_3
        elif ctx == 4:
            s.reset(user_id)
            return ms.MSG_END
    elif ss_type == st.Type.BN_CREATE_TRACK2:
        if ctx == 1:
            return ms.MSG_BN_CREATE_T2_1
        elif ctx == 2:
            return ms.MSG_BN_CREATE_T2_2
        elif ctx == 3:
            return ms.MSG_BN_CREATE_T2_3
        elif ctx == 4:
            s.reset(user_id)
            return ms.MSG_END
    elif ss_type == st.Type.BN_CREATE_TRACK3:
        if ctx == 1:
            return ms.MSG_BN_CREATE_T3_1
        elif ctx == 2:
            return ms.MSG_BN_CREATE_T3_2
        elif ctx == 3:
            s.reset(user_id)
            return ms.MSG_END
    elif ss_type == st.Type.BN_CREATE_TRACK5:
        if ctx == 1:
            return ms.MSG_BN_CREATE_T5_1
        elif ctx == 2:
            return ms.MSG_BN_CREATE_T5_2
        elif ctx == 3:
            s.reset(user_id)
            return ms.MSG_END


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
    app.run(host="localhost", port=8000)
