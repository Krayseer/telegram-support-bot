import telebot
import os
from dotenv import load_dotenv
from telebot import types
from neural_service import handle
from message_provider import get_message_by_key
from gpt_service import handleMessageToQuestion, handleMessageToAnswer

# Загрузка виртуальных переменных
load_dotenv()

# Инициализация бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

chat_anykeyers = '-1001918550413'
chat_test = '-1001990006454'


# Обработка команд
@bot.message_handler(commands=['start'])
def send_welcome():
    bot.send_message(chat_test, get_message_by_key('start.bot'))


# Обработка сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    yesButton = types.InlineKeyboardButton(text="Да", callback_data="In_yesButton")
    noButton = types.InlineKeyboardButton(text="Нет", callback_data="In_noButton")
    nextButton = types.InlineKeyboardButton(text="Следующий", callback_data="In_nextButton")
    keyboard_inline = types.InlineKeyboardMarkup().add(yesButton, noButton, nextButton)

    question = handleMessageToQuestion(message.text)
    generateAns = handle(question)
    answer = handleMessageToAnswer(generateAns)

    bot.send_message(chat_test,
                     f'question: {question}\n\nanswer: {answer}',
                     reply_markup=keyboard_inline)


# Запуск бота
if __name__ == '__main__':
    bot.infinity_polling()
