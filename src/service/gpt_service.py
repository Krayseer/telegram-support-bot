import requests
from src import messages, config


def handleMessageToQuestion(text):
    json_data = {
        "text": f'{messages.get_message_by_key("message.to-question")}: {text}'
    }
    return handleMessage(json_data)


def handleMessageToAnswer(text):
    json_data = {
        "text": f'{messages.get_message_by_key("message.to-answer")}: {text}',
        "time": "6000"
    }
    return handleMessage(json_data)


def handleMessage(json_data):
    return requests.post(config.GPT_URL, json=json_data).text
