import logging
import sys
import random
import json

import schedule as schedule
from flask import Flask, abort, request, Response
from flask_sqlalchemy import SQLAlchemy
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, FollowEvent, UnfollowEvent,
)
from werkzeug.middleware.proxy_fix import ProxyFix

import models.catcher as catcher
import models.status as st
import models.session as ss
import models.user as user
import config
from database.database import init_db, db, get_db_uri
import const.message as ms
import slack
import models


def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()

    init_db(app)

    return app


app = create_app()

with app.app_context():
    db.create_all()

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
display_name = {}

schedule.every(1).week.do(cs.refresh)


@app.route('/test', methods=["GET"])
def test():
    users = models.User.query.all()
    print(users)
    return Response(json.dumps({"status": "OK"}), mimetype='application/json')


@app.route('/', methods=["POST"])
def index():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    # for challenge of slack api
    if 'challenge' in data:
        token = str(data['challenge'])
        return Response(token, mimetype='text/plane')
    # for events which you added
    if 'event' in data:
        event = data['event']
        app.logger.info(event)
        reply_contact(event)
    return 'OK'


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


@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    msg = ms.MSG_DEFAULT
    msg.template.title = profile.display_name + 'さん、はじめまして！\n' \
                                                '友達追加ありがとうございます！'
    line_bot_api.reply_message(event.reply_token, msg)
    msg.template.title = 'メッセージありがとうございます！'
    display_name[user_id] = profile.display_name
    slack.send_message(f'{profile.display_name}さんが追加しました！')


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    user_id = event.source.user_id
    slack.send_message(f'{display_name.get(user_id)}さんがブロックしました...')


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    user_id = event.source.user_id

    s.register(user_id)
    ctx = s.get_context(user_id)
    ss_type = s.get_type(user_id)

    if ctx != 0 and text == ms.KEY_END:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_END))
        s.reset(user_id)
    elif ctx == 0:
        handle_ctx0(event)
    elif ss_type == st.Type.CATCH_REC and text in ['Yes', 'No']:
        handle_catcher_rec(event)
    elif ss_type == st.Type.CONTACT:
        profile = line_bot_api.get_profile(user_id)
        slack.send_msg_to_thread(profile.display_name, text, user.get_thread_by_id(user_id))
    elif text == '次':
        handle_next(event)
    elif text in (ms.MSG_BN_CREATE_3_1, ms.MSG_BN_CREATE_3_2, ms.MSG_BN_CREATE_3_3, ms.MSG_BN_CREATE_3_5):
        handle_route_bn_create(event)


def handle_next(event):
    user_id = event.source.user_id
    msg = route_next(user_id)
    if isinstance(msg, str):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
    else:
        line_bot_api.reply_message(event.reply_token, msg)


def handle_ctx0(event):
    text = event.message.text
    user_id = event.source.user_id
    if text == ms.KEY_SELF_REFLECTION:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_SELF_REFLECTION))
    elif text == ms.KEY_BN_CREATE:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_BN_CREATE))
        line_bot_api.push_message(user_id, TextSendMessage(text=ms.MSG_BN_CREATE_1))
        s.set_context(user_id, 2)
        s.set_type(user_id, st.Type.BN_CREATE)
    elif text == ms.KEY_CATCHER:
        cs.register(user_id)
        schedule.run_pending()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_CATCHER))
        msg = ms.MSG_CATCHER_CONFIRM
        tag, q = cs.get_question(user_id)
        msg.alt_text = q
        msg.template.text = q
        line_bot_api.push_message(user_id, msg)
        s.set_type(user_id, st.Type.CATCH_REC)
        s.set_context(user_id, 1)
    elif text == ms.KEY_CONTACT:
        profile = line_bot_api.get_profile(user_id)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_CONTACT_DEFAULT))
        s.set_context(user_id, 1)
        s.set_type(user_id, st.Type.CONTACT)
        res = slack.start_contact(profile.display_name)
        user.register_thread(user_id, res['message']['ts'])
    else:
        line_bot_api.reply_message(event.reply_token, ms.MSG_DEFAULT)


def handle_catcher_rec(event):
    user_id = event.source.user_id
    text = event.message.text
    if cs.catcher_question[user_id] is None:
        if text == 'No':
            cs.exclude_tag(user_id, cs.used_tags[user_id][-1])
        else:
            rec = cs.get_rec(user_id)
            if rec is not None:
                send_rec(event, user_id, rec)
                return
    else:
        if text == 'Yes':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_CATCHER_END))
            s.reset(user_id)
            return
        elif text == 'No':
            cs.cand_by_user[user_id].remove(cs.catcher_question[user_id])
        rec = cs.get_rec(user_id)
        if rec is not None:
            send_rec(event, user_id, rec)
            return
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
        cs.catcher_question[user_id] = None
        msg = ms.MSG_CATCHER_CONFIRM
        msg.alt_text = q
        msg.template.text = q
        line_bot_api.reply_message(event.reply_token, msg)


def handle_route_bn_create(event):
    user_id = event.source.user_id
    text = event.message.text
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


def send_rec(event, user_id, rec):
    cs.catcher_question[user_id] = rec
    msg = ms.MSG_CATCHER_CONFIRM
    msg.alt_text = ms.MSG_CATCHER_CONFIRM_TEXT
    msg.template.text = ms.MSG_CATCHER_CONFIRM_TEXT
    line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="catcher profile",
                                                                  contents=ms.get_catcher(rec)))
    line_bot_api.push_message(user_id, msg)


def route_bn_create(user_id: str):
    ss_type = s.get_type(user_id)
    ctx = s.get_context(user_id)
    s.increment_context(user_id)

    if ss_type in ms.type_dict:
        bn_dict = ms.type_dict[ss_type]

    if ctx in bn_dict:
        if bn_dict[ctx] == ms.MSG_END:
            s.reset(user_id)
        return bn_dict[ctx]


def route_next(user_id: str):
    ctx = s.get_context(user_id)
    ss_type = s.get_type(user_id)
    if ss_type == st.Type.BN_CREATE:
        s.increment_context(user_id)
        if ctx == 2:
            return ms.MSG_BN_CREATE_2
        elif ctx == 3:
            return ms.MSG_BN_CREATE_3
    elif ss_type in (
            st.Type.BN_CREATE_TRACK1, st.Type.BN_CREATE_TRACK2, st.Type.BN_CREATE_TRACK3, st.Type.BN_CREATE_TRACK5):
        return route_bn_create(user_id)


def reply_contact(event):
    if 'bot_id' not in event:
        thread_ts = event['thread_ts']
        user_id = user.get_user_by_thread_ts(thread_ts)
        msg = event['text']
        line_bot_api.push_message(user_id, TextSendMessage(text=msg))


if __name__ == "__main__":
    # app.run()
    # db.create_all()
    app.run(host='0.0.0.0')
