from dotenv import load_dotenv
import os

load_dotenv()

SLACK_TOKEN = os.getenv('SLACK_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
