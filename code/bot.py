import telebot
import os
from dotenv import load_dotenv
from telebot import types
from neural_service import handle
from message_provider import get_message_by_key

# Загрузка виртуальных переменных
load_dotenv()

# Инициализация бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


# Обработка команд
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, get_message_by_key('start.bot'))


# Обработка сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    yesButton = types.InlineKeyboardButton(text="Да", callback_data="In_yesButton")
    noButton = types.InlineKeyboardButton(text="Нет", callback_data="In_noButton")
    nextButton = types.InlineKeyboardButton(text="Следующий", callback_data="In_nextButton")
    keyboard_inline = types.InlineKeyboardMarkup().add(yesButton, noButton, nextButton)

    bot.reply_to(message, handle(message.text), reply_markup=keyboard_inline)


# Запуск бота
if __name__ == '__main__':
    bot.infinity_polling()
