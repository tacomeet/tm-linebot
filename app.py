import logging
import sys
import json
import time
from datetime import datetime, timedelta

import schedule as schedule
from flask import Flask, abort, request, Response
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, UnfollowEvent,
)
from sqlalchemy.exc import IntegrityError
from werkzeug.middleware.proxy_fix import ProxyFix

import text_handler as th
from models.status_type import StatusType
import models.status_type as st
import config
from database.database import init_db, db
import message as ms
import slack
import models
from models import User
import catcher_rec as cr
import spreadsheet
import const.color as color


def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_db_uri()

    init_db(app)

    return app


app = create_app()

with app.app_context():
    db.create_all()

workbook = config.connect_gspread()
worksheet_goal_rate = workbook.worksheet('Goal_Rate')

logging.basicConfig(level=logging.WARN, stream=sys.stdout)

channel_access_token = config.LINE_CHANNEL_ACCESS_TOKEN
channel_secret = config.LINE_CHANNEL_SECRET
if channel_secret is None or channel_access_token is None:
    app.logger.error('Specify LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN in .env file')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# somehow RuntimeError happens
# cr.setup_catcher_tag()
schedule.every(1).week.do(cr.refresh_catcher_tag)


@app.route('/health', methods=["GET"])
def health():
    return 'OK'


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
        reply_to_user(event)
    return 'OK'


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)

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

    # send welcome message on LINE
    msg = ms.default.MENU
    msg.template.title = profile.display_name + 'さん、はじめまして！\n' \
                                                '友達追加ありがとうございます！'
    msg.template.title = 'メッセージありがとうございます！'
    line_bot_api.reply_message(event.reply_token, msg)

    # add user to db
    user = User(id=user_id, name=profile.display_name)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        slack.refollow(user.get_name())
        return

    # send message to slack
    slack.follow(user.get_name())


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    user_id = event.source.user_id
    user = User.query.get(user_id)
    slack.block(user.get_name())


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    user_id = event.source.user_id

    # get user from db
    user = User.query.get(user_id)
    if user is None:
        profile = line_bot_api.get_profile(user_id)
        user = User(id=user_id, name=profile.display_name)
        db.session.add(user)
        db.session.commit()
        user = User.query.get(user_id)

    last_handled_timestamp = user.get_last_handled_timestamp()
    if last_handled_timestamp is not None:
        diff = datetime.now() - last_handled_timestamp
        if diff < timedelta(seconds=2):
            return
    user.set_last_handled_timestamp()
    db.session.commit()

    ss_stage = user.get_session_stage()
    ss_type = user.get_session_type()

    if ss_stage != 0 and text == ms.default.KEY_END:
        spreadsheet.record_goal_rate(user, worksheet_goal_rate, False)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.default.END))
        if ss_type != StatusType.CONTACT:
            user.set_answer_msg(text)
            slack.send_msg_to_other_thread(user, color=color.INTERRUPTION)
        user.reset()
        cr.reset(user_id)
    elif ss_stage == 0:
        th.stage0(line_bot_api, user, event)
    elif ss_type == StatusType.CATCH_REC:
        th.catcher_rec(line_bot_api, user, event)
    elif ss_type == StatusType.CONTACT:
        slack.send_msg_to_contact_thread(user.get_name(), text, user.get_thread_ts_contact())
    elif st.is_included(StatusType.SELF_REF, ss_type):
        th.self_ref(line_bot_api, user, event)
    elif st.is_included(StatusType.BN_CREATE, ss_type):
        th.bn_create(line_bot_api, user, event)
    db.session.commit()


def reply_to_user(event):
    if 'bot_id' not in event and 'thread_ts' in event:
        thread_ts = event['thread_ts']
        channel = event['channel']
        user = None
        if channel == config.CONTACT_CHANNEL_ID:
            user = User.query.filter_by(thread_ts_contact=thread_ts).first()
        elif channel == config.OTHER_CHANNEL_ID:
            user = User.query.filter_by(thread_ts_other=thread_ts).first()
        if user is None:
            return
        user_id = user.get_id()
        msg = event['text']
        line_bot_api.push_message(user_id, TextSendMessage(text=msg))


if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0')
