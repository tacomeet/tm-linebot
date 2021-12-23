import os

import requests

TOKEN = os.getenv('SLACK_TOKEN')
if TOKEN is None:
    print('SLACK_TOKEN is not set')
    exit(1)
CHANNEL = 'api-test'

URL = "https://slack.com/api/chat.postMessage"
HEADERS = {"Authorization": "Bearer " + TOKEN}


def send_msg(msg):
    data = {
        'channel': CHANNEL,
        'text': msg
    }
    requests.post(URL, headers=HEADERS, data=data)
