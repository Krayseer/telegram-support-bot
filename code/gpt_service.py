import os

import requests
from dotenv import load_dotenv
from message_provider import get_message_by_key

load_dotenv()


def handleMessageToQuestion(text):
    json_data = {
        "text": f'{get_message_by_key("message.to-question")}: {text}'
    }
    return handleMessage(json_data)


def handleMessageToAnswer(text):
    json_data = {
        "text": f'{get_message_by_key("message.to-answer")}: {text}',
        "time": "6000"
    }
    return handleMessage(json_data)


def handleMessage(json_data):
    url = os.getenv('GPT_URL')
    return requests.post(url, json=json_data).text
