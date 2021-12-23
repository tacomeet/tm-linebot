import requests

import config

CHANNEL = 'api-test'

URL = "https://slack.com/api/chat.postMessage"
HEADERS = {"Authorization": "Bearer " + config.SLACK_TOKEN}


def send_msg(msg):
    data = {
        'channel': CHANNEL,
        'text': msg
    }
    requests.post(URL, headers=HEADERS, data=data)
