import os

import requests
from dotenv import load_dotenv
from message_provider import get_message_by_key

load_dotenv()


def handleMessageToQuestion(text):
    return handleMessage(f'{get_message_by_key("message.to-question")}: {text}')


def handleMessageToAnswer(text):
    return handleMessage(f'{get_message_by_key("message.to-answer")}: {text}')


def handleMessage(data):
    url = os.getenv('GPT_URL')
    return requests.post(url, json={"text": data}).text
