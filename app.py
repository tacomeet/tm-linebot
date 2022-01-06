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
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, FollowEvent, UnfollowEvent,
)
from sqlalchemy.exc import IntegrityError
from werkzeug.middleware.proxy_fix import ProxyFix

from models.status_type import StatusType
import config
from database.database import init_db, db
import const.message as ms
import slack
import models
from models import User
import catcher_rec as cr


def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_db_uri()

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

# somehow RuntimeError happens
# cr.setup_catcher_tag()
schedule.every(1).week.do(cr.refresh_catcher_tag)


@app.route('/test', methods=["GET"])
def test():
    users = models.User.query.all()
    if len(users) == 0:
        return 'no user'
    return Response(json.dumps(users[0].__dict__), mimetype='application/json')


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
    msg = ms.MSG_DEFAULT
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

    if ss_stage != 0 and text == ms.KEY_END:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_END))
        user.reset()
        cr.reset(user_id)
    elif ss_stage == 0:
        handle_stage0(user, event)
    elif ss_type == StatusType.CATCH_REC and text in ['Yes', 'No']:
        handle_catcher_rec(user, event)
    elif ss_type == StatusType.CONTACT:
        profile = line_bot_api.get_profile(user_id)
        slack.send_msg_to_thread(profile.display_name, text, user.get_thread_ts())
    elif text == '次':
        handle_next(user, event)
    elif text in (ms.MSG_BN_CREATE_3_1, ms.MSG_BN_CREATE_3_2, ms.MSG_BN_CREATE_3_3, ms.MSG_BN_CREATE_3_5):
        handle_route_bn_create(user, event)
    db.session.commit()


def handle_next(user, event):
    msg = route_next(user)
    if isinstance(msg, str):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
    else:
        line_bot_api.reply_message(event.reply_token, msg)


def handle_stage0(user, event):
    text = event.message.text
    user_id = event.source.user_id
    if text == ms.KEY_SELF_REFLECTION:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_SELF_REFLECTION))
        slack.start_self_rec(user.get_name())
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


def handle_catcher_rec(user, event):
    user_id = event.source.user_id
    text = event.message.text
    possible_to_match = True
    if user.get_is_matched():
        if text == 'Yes':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_CATCHER_END))
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
            send_rec(user, event, catcher_id)
            return
    tag_id, question = cr.get_question(user_id)
    if not tag_id:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ms.MSG_CATCHER_SORRY))
        cr.reset(user_id)
        user.reset()
    else:
        user.last_question_id = tag_id
        user.set_is_matched(False)
        msg = ms.MSG_CATCHER_CONFIRM
        msg.alt_text = question
        msg.template.text = question
        line_bot_api.reply_message(event.reply_token, msg)


def handle_route_bn_create(user, event):
    text = event.message.text
    user.set_session_stage(1)
    if text == ms.MSG_BN_CREATE_3_1:
        user.set_session_type(StatusType.BN_CREATE_TRACK1)
    elif text == ms.MSG_BN_CREATE_3_2:
        user.set_session_type(StatusType.BN_CREATE_TRACK2)
    elif text == ms.MSG_BN_CREATE_3_3:
        user.set_session_type(StatusType.BN_CREATE_TRACK3)
    elif text == ms.MSG_BN_CREATE_3_5:
        user.set_session_type(StatusType.BN_CREATE_TRACK5)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=route_bn_create(user)))


def send_rec(user: User, event, catcher_id):
    user.set_last_question_id(catcher_id)
    user.set_is_matched(True)
    msg = ms.MSG_CATCHER_CONFIRM
    msg.alt_text = ms.MSG_CATCHER_CONFIRM_TEXT
    msg.template.text = ms.MSG_CATCHER_CONFIRM_TEXT
    line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="catcher profile",
                                                                  contents=ms.get_catcher(catcher_id)))
    line_bot_api.push_message(user.id, msg)


def route_bn_create(user: User):
    ss_stage = user.get_session_stage()
    ss_type = user.get_session_type()
    user.increment_session_stage()

    bn_dict = ms.type_dict[ss_type]
    if ss_stage in bn_dict:
        if bn_dict[ss_stage] == ms.MSG_END:
            user.reset()
        return bn_dict[ss_stage]


def route_next(user: User):
    ss_stage = user.get_session_stage()
    ss_type = user.get_session_type()
    if ss_type == StatusType.BN_CREATE:
        user.increment_session_stage()
        if ss_stage == 2:
            return ms.MSG_BN_CREATE_2
        elif ss_stage == 3:
            return ms.MSG_BN_CREATE_3
    elif ss_type in (
            StatusType.BN_CREATE_TRACK1, StatusType.BN_CREATE_TRACK2, StatusType.BN_CREATE_TRACK3,
            StatusType.BN_CREATE_TRACK5):
        return route_bn_create(user)


def reply_contact(event):
    if 'bot_id' not in event:
        thread_ts = event['thread_ts']
        user = User.query.filter_by(thread_ts=thread_ts).first()
        user_id = user.get_id()
        msg = event['text']
        line_bot_api.push_message(user_id, TextSendMessage(text=msg))


if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0')
