import telebot
import os
from dotenv import load_dotenv
from transformers import pipeline

from message_provider import MessageProvider

# Загрузка виртуальных переменных
load_dotenv()

# Инициализация бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
message_provider = MessageProvider()

# Модель
model_pipeline = pipeline(
    task='question-answering',
    model='timpal0l/mdeberta-v3-base-squad2'
)

# Контекст, далее это будет файл
context = ('Пачки скидываются потому, что'
         ' не читались этикетки'
         ' У вас закончились вычислительные единицы.'
         ' Доступ к бесплатным ресурсам не гарантирован.'
         ' Были частые сбросы за пинцет. Увеличили количество обрабатываемых кадров для считывания qr-кодов.'
         ' Сбросы за пинцет прекратились.')


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
    return model_pipeline(question=message, context=context)


# Запуск бота
if __name__ == '__main__':
    bot.infinity_polling()
