from slack_sdk import WebClient

import config


# Load channel from config?
channel = '#api'
token = config.SLACK_TOKEN
client = WebClient(token=token)


def send_message(msg, ts=None):
    return client.chat_postMessage(channel=channel, text=msg, thread_ts=ts)


def start_contact(name):
    return send_message(name + 'さんからお問い合わせがありました！')


def send_msg_to_thread(name, content, ts):
    send_message(name + 'さんからのお問い合わせ内容：\n' + content, ts)
