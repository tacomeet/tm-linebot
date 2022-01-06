from slack_sdk import WebClient

import config

# Load channel from config?
CHANNEL_CONTACT = '#line-contact'
CHANNEL_OTHER = '#line-other'
token = config.SLACK_TOKEN
client = WebClient(token=token)


def send_message(msg, ts=None, channel=CHANNEL_OTHER):
    return client.chat_postMessage(channel=channel, text=msg, thread_ts=ts)


def start_contact(name):
    return send_message(name + 'さんからお問い合わせがありました！', CHANNEL_CONTACT)


def send_msg_to_thread(name, content, ts):
    send_message(name + 'さんからのお問い合わせ内容：\n' + content, ts)


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
