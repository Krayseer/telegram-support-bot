import json
import telebot
import config
import messages
import source.service.neural_service as neural_service
import source.service.gpt_service as gpt_service
import source.service.db_service as db_service

BOT_TOKEN = config.BOT_TOKEN
CHAT_ID = config.TELEGRAM_CHAT_ID
bot = telebot.TeleBot(BOT_TOKEN)


def create_inline_keyboard(question):
    yesButton = telebot.types.InlineKeyboardButton(text="Да", callback_data=json.dumps(
        {'name': 'YES', 'question': question}
    ))
    noButton = telebot.types.InlineKeyboardButton(text="Нет", callback_data=json.dumps(
        {'name': 'NO', 'question': question}
    ))
    nextButton = telebot.types.InlineKeyboardButton(text='В тех-поддержку', callback_data=json.dumps(
        {'name': 'TO_ADMIN', 'question': question}
    ))
    return telebot.types.InlineKeyboardMarkup().add(yesButton, noButton, nextButton)


@bot.message_handler(commands=['start'])
def send_welcome():
    bot.send_message(CHAT_ID, messages.get_message_by_key('start.bot'))


# Обработка авторизации админа
@bot.message_handler(commands=['login'])
def login(message):
    # Проверяем, является ли пользователь админом
    if db_service.is_admin(message.from_user.id):
        bot.send_message(message.from_user.id, "Вы уже являетесь администратором.")
    else:
        # Проверяем наличие аргумента (секретного ключа)
        if len(message.text.split()) == 2:
            secret_key = message.text.split()[1]

            # Ваш секретный ключ для администратора
            admin_secret_key = "admin4444"

            # Проверяем, является ли введенный ключ секретным ключом администратора
            if secret_key == admin_secret_key:
                # Добавляем пользователя в список администраторов (может быть сохранено в базе данных)
                db_service.add_admin(message.from_user.id)
                bot.send_message(message.from_user.id, "Вы успешно авторизованы как администратор.")
            else:
                bot.send_message(message.from_user.id, "Неверный секретный ключ.")
        else:
            bot.send_message(message.from_user.id, "Используйте команду в формате /login <секретный_ключ>")



# Обработка выхода из админа
@bot.message_handler(commands=['logout'])
def logout(message):
    # Проверяем, является ли пользователь админом
    if db_service.is_admin(message.from_user.id):
        db_service.remove_admin(message.from_user.id)
        bot.send_message(message.from_user.id, "Вы потеряли права администратора")
    else:
        bot.send_message(message.from_user.id, "Вы не являетесь администратором.")


# Выводит все необработанные заявки от пользователей
@bot.message_handler(commands=['get_all'])
def get_all(message):
    # Проверяем, является ли отправитель администратором
    if db_service.is_admin(message.from_user.id):
        # Получаем все заявки и отправляем их администратору
        all_requests = db_service.get_WAIT_requests()
        # Проверяем имеются ли заявки для администраторов
        if all_requests:
            for request in all_requests:
                request_id = request[0]
                request_text = request[1]
                process_button = telebot.types.InlineKeyboardButton(
                    text="Обработать заявку",
                    callback_data=json.dumps(
                        {'name': 'PROCESSING',
                         'question': request_text,
                         'request_id': request_id}
                    ))

                bot.send_message(message.from_user.id, f"ID заявки: {request_id}\nВопрос: {request_text}",
                                 reply_markup=telebot.types.InlineKeyboardMarkup().add(process_button))
        else:
            bot.send_message(message.from_user.id, "Необработанных заявок не найдено.")
    else:
        bot.send_message(message.from_user.id, "У вас нет прав для выполнения этой команды.")


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if db_service.is_admin(message.from_user.id):
        chat_state = db_service.get_chat_state(message.chat.id)
        request_id = chat_state[1]
        question = db_service.find_question_by_id(request_id)[1]
        bot.send_message(CHAT_ID, f'Вопрос: {question}\n\nОтвет от администратора: {message.text}')
        bot.send_message(message.from_user.id, "Ваш ответ отправлен.")
        db_service.update_request_status(request_id)
        db_service.remove_chat_state(message.from_user.id)
    else:
        question = message.text
        # question_to_handle = gpt_service.handleMessageToQuestion(question)
        # result = gpt_service.handleMessageToAnswer(neural_service.generate_answer(question_to_handle))
        result = f'Обработанное сообщение: {question}'
        buttons = create_inline_keyboard(question)
        bot.send_message(CHAT_ID, f'Вопрос: {question}\n\nОтвет: {result}', reply_markup=buttons)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    call_data = json.loads(call.data)
    name = call_data['name']
    question = call_data['question']

    if name == 'YES':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text)
        db_service.add_question(question, 'COMPLETE', call.message.message_id)

    elif name == 'NO':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Вопрос: {question}\n\nВопрос обрабатывается...')
        # question_to_handle = gpt_service.handleMessageToQuestion(question)
        # result = gpt_service.handleMessageToAnswer(neural_service.generate_answer(question_to_handle))
        result = f'Обработанное сообщение: {question}'
        buttons = create_inline_keyboard(question)
        bot.edit_message_text(chat_id=CHAT_ID, message_id=call.message.message_id,
                              text=f'Вопрос: {question}\n\nОтвет: {result}', reply_markup=buttons)

    elif name == 'TO_ADMIN':
        db_service.add_question(question, 'WAIT', call.message.message_id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Вопрос: {question}\n\nОжидается ответ администратора...')

    elif name == 'PROCESSING':
        db_service.add_chat_state(call.message.chat.id, call_data['request_id'])
        bot.send_message(call.message.chat.id, f'Введите ответ на вопрос: {question}')


if __name__ == '__main__':
    bot.infinity_polling()
