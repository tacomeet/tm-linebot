from slack_sdk import WebClient

import config
import const.color as color

# Load channel from config?
CHANNEL_CONTACT = '#line'
CHANNEL_OTHER = '#line-other'
token = config.SLACK_TOKEN
client = WebClient(token=token)


def send_message(msg, ts=None, channel=CHANNEL_OTHER, attachments=None):
    return client.chat_postMessage(channel=channel, text=msg, thread_ts=ts, attachments=attachments)


def start_contact(name):
    return send_message(name + 'さんからお問い合わせがありました！', channel=CHANNEL_CONTACT)


def send_msg_to_contact_thread(name, content, ts):
    send_message(name + 'さんからのお問い合わせ内容：\n' + content, ts, channel=CHANNEL_CONTACT)


def send_msg_to_other_thread(user, color=color.SUCCESS):
    _send_msg_to_other_thread(user.get_question_msg(), user.get_answer_msg(), user.get_thread_ts_other(), color)


def _send_msg_to_other_thread(question, answer, ts, color):
    send_message(question, ts=ts, attachments=[{"text": answer, "color": color}])


def follow(name):
    return send_message(f'{name}さんが追加しました...')


def refollow(name):
    return send_message(f'{name}さんが再追加しました...')


def block(name):
    return send_message(f'{name}さんがブロックしました...')


def start_self_rec(name):
    return send_message(name + 'さんが自己分析を開始しました！')


def start_bn_creation(name):
    return send_message(name + 'さんがBN作成を開始しました！')


def start_catcher_rec(name):
    return send_message(name + 'さんがロールモデルマッチングを始めました！')


def tag_missing(tag_id):
    return send_message(f'{tag_id}番のタグが見つかりませんでした...')
