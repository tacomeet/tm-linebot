import logging
import sys
import json

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

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

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


@app.route('/test', methods=["GET"])
def test():
    users = models.User.query.all()
    if len(users) == 0:
        return 'no user'
    return Response(json.dumps(users[0].__dict__), mimetype='application/json')


@app.route('/test/gspread', methods=["GET"])
def test_gspread():
    worksheet = workbook.worksheet('user')
    df = spreadsheet.get_worksheet_as_dataframe(worksheet)
    print(df)
    return Response(df.to_json(), mimetype='application/json')


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

    ss_stage = user.get_session_stage()
    ss_type = user.get_session_type()

    if ss_stage != 0 and text == ms.default.KEY_END:
        spreadsheet.record_goal_rate(user, worksheet_goal_rate, False)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.default.END))
        if ss_type != StatusType.CONTACT:
            slack.send_msg_to_other_thread(user.get_name(), text, user.get_thread_ts_other())
        user.reset()
        cr.reset(user_id)
    elif ss_stage == 0:
        th.stage0(line_bot_api, user, event)
    elif ss_type == StatusType.CATCH_REC:
        slack.send_msg_to_other_thread(user.get_name(), text, user.get_thread_ts_other())
        th.catcher_rec(line_bot_api, user, event)
    elif ss_type == StatusType.CONTACT:
        slack.send_msg_to_contact_thread(user.get_name(), text, user.get_thread_ts_contact())
    elif st.is_included(StatusType.SELF_REF, ss_type):
        slack.send_msg_to_other_thread(user.get_name(), text, user.get_thread_ts_other())
        th.self_ref(line_bot_api, user, event)
    elif st.is_included(StatusType.BN_CREATE, ss_type):
        slack.send_msg_to_other_thread(user.get_name(), text, user.get_thread_ts_other())
        th.bn_create(line_bot_api, user, event)
    db.session.commit()


def reply_contact(event):
    if 'bot_id' not in event and 'thread_ts' in event:
        thread_ts = event['thread_ts']
        user = User.query.filter_by(thread_ts_contact=thread_ts).first()
        user_id = user.get_id()
        msg = event['text']
        line_bot_api.push_message(user_id, TextSendMessage(text=msg))


if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0')
