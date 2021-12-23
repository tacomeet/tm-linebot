from slack_sdk import WebClient
import requests

import config
import contact


# Load channel from config?
channel = '#api'
token = config.SLACK_TOKEN
client = WebClient(token=token)


def start_contact(name):
    return client.chat_postMessage(channel=channel, text=name + 'さんからお問い合わせがありました！')
        
def send_msg_to_thread(name, content, ts):
    client.chat_postMessage(channel=channel, text=name + 'さんからのお問い合わせ内容：\n' + content, thread_ts=ts)
