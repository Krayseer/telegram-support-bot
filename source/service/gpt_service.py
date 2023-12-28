import config
import requests
import source.messages as messages

gpt_url = config.GPT_URL


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
    url = gpt_url + '/process'
    return requests.post(url, json=json_data).text
