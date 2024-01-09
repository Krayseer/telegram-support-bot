import re

import telebot
from src import config
import messages
from src.service import db_service
from src.service import neural_service
from src.service import gpt_service

bot = telebot.TeleBot(config.BOT_TOKEN)

# Создаем таблицы в бд
db_service.create_tables_for_db()


# Получить из сообщения текст вопроса в кавычках
def extract_question_from_message(msg):
    match = re.search(r'Вопрос: "(.*?)"', msg)
    return match.group(1) if match else None


# Получить из сообщения идентификатор заявки
def extract_id_message_from_message(msg):
    match = re.search(r'ID заявки: "(.*?)"', msg)
    return match.group(1) if match else None


# Получить кнопки "Да/Нет/На администратора"
def create_inline_keyboard():
    yesButton = telebot.types.InlineKeyboardButton(text=messages.get_message_by_key('commons.yes'), callback_data='YES')
    noButton = telebot.types.InlineKeyboardButton(text=messages.get_message_by_key('commons.no'), callback_data='NO')
    nextButton = telebot.types.InlineKeyboardButton(text=messages.get_message_by_key('commons.to-admin'),
                                                    callback_data='TO_ADMIN')
    return telebot.types.InlineKeyboardMarkup().add(yesButton, noButton, nextButton)


@bot.message_handler(commands=['start'])
def send_welcome():
    bot.send_message(config.TELEGRAM_CHAT_ID, messages.get_message_by_key('start.bot'))


# Обработка авторизации администратора
@bot.message_handler(commands=['login'])
def login(message):
    if len(message.text.split()) != 2:
        bot.send_message(message.chat.id, messages.get_message_by_key("login.invalid.format"))
        return
    if message.text.split()[1] != config.ADMIN_SECRET:
        bot.send_message(message.chat.id, messages.get_message_by_key('login.invalid.secret-key'))
        return
    db_service.add_admin(message.chat.id)
    bot.send_message(message.chat.id, messages.get_message_by_key('login.success'))


# Обработка удаления администратора
@bot.message_handler(commands=['logout'])
def logout(message):
    if not db_service.is_user_admin(message.chat.id):
        bot.send_message(message.chat.id, messages.get_message_by_key('logout.error'))
        return
    db_service.remove_admin(message.chat.id)
    bot.send_message(message.chat.id, messages.get_message_by_key('logout.success'))


# Выводит все необработанные заявки от пользователей
@bot.message_handler(commands=['tasks'])
def get_tasks(message):
    if not db_service.is_user_admin(message.chat.id):
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")
        return
    all_requests = db_service.get_all_tasks()
    if not all_requests:
        bot.send_message(message.chat.id, "Необработанных заявок не найдено.")
        return
    for request in all_requests:
        process_button = telebot.types.InlineKeyboardButton(text="Обработать заявку", callback_data='PROCESSING')
        bot.send_message(message.chat.id, f'ID заявки: "{request[3]}"\nВопрос: "{request[1]}"',
                         reply_markup=telebot.types.InlineKeyboardMarkup().add(process_button))


@bot.message_handler(func=lambda message: message.is_topic_message)
def handle_messages_is_topic(message):
    question = message.text
    result = neural_service.generate_answer(question) if config.GPT_URL is None else (
        gpt_service.handleMessageToAnswer(
            neural_service.generate_answer(gpt_service.handleMessageToQuestion(question))
        )
    )
    bot.send_message(config.TELEGRAM_CHAT_ID, f'Вопрос: "{question}"\n\nОтвет: {result}',
                     reply_markup=create_inline_keyboard())


@bot.message_handler(func=lambda message: not message.is_topic_message and db_service.is_user_admin(message.chat.id))
def handle_message(message):
    question = db_service.get_chat_state(message.chat.id)[1]
    id_message = extract_id_message_from_message(question)
    bot.edit_message_text(chat_id=config.TELEGRAM_CHAT_ID, message_id=id_message,
                          text=f'{question}"\n\nОтвет от администратора: {message.text}')
    bot.send_message(config.TELEGRAM_CHAT_ID, f'Ответ от администратора: {message.text}',
                     reply_to_message_id=id_message)
    bot.send_message(message.chat.id, "Ваш ответ отправлен.")
    db_service.update_request_status(id_message)
    db_service.remove_chat_state(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    question = extract_question_from_message(call.message.text)

    if call.data == 'YES':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text)
        db_service.add_question(question, 'COMPLETE', call.message.message_id)

    elif call.data == 'NO':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Вопрос: "{question}"\n\nВопрос обрабатывается...')
        result = gpt_service.handleMessageToAnswer(
            neural_service.generate_answer(gpt_service.handleMessageToQuestion(question))
        )
        bot.edit_message_text(chat_id=config.TELEGRAM_CHAT_ID, message_id=call.message.message_id,
                              text=f'Вопрос: "{question}"\n\nОтвет: {result}', reply_markup=create_inline_keyboard())

    elif call.data == 'TO_ADMIN':
        db_service.add_question(question, 'WAIT', call.message.message_id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Вопрос: "{question}"\n\nОжидается ответ администратора...')

    elif call.data == 'PROCESSING':
        db_service.add_chat_state(call.message.chat.id, call.message.text)
        bot.send_message(call.message.chat.id, f'Введите ответ на вопрос: {question}')


if __name__ == '__main__':
    bot.infinity_polling()
