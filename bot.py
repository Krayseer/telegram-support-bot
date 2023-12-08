import telebot
import os
from dotenv import load_dotenv

from message_provider import MessageProvider

# Загрузка виртуальных переменных
load_dotenv()

# Инициализация бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
message_provider = MessageProvider()


# Обработка команд
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, message_provider.get_message_by_key('start.bot'))


# Обработка сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, handleRequest(message.text))


# Получить ответ на запрос пользователя
def handleRequest(message):
    return message_provider.get_message_by_key('redirect.admin')


# Запуск бота
if __name__ == '__main__':
    bot.infinity_polling()
