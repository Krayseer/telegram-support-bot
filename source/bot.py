import telebot
import config
import source.service.neural_service as neural_service
import messages
import source.service.gpt_service as gpt_service
import source.service.db_service as db_service

# Инициализация бота
BOT_TOKEN = config.BOT_TOKEN
CHAT_ID = config.TELEGRAM_CHAT_ID
bot = telebot.TeleBot(BOT_TOKEN)


# Обработка команд
@bot.message_handler(commands=['start'])
def send_welcome():
    bot.send_message(CHAT_ID, messages.get_message_by_key('start.bot'))


# Обработка сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    question_to_handle = gpt_service.handleMessageToQuestion(message.text)
    result = gpt_service.handleMessageToAnswer(neural_service.generate_answer(question_to_handle))
    bot.send_message(CHAT_ID, f'Вопрос: {question_to_handle}\n\nОтвет: {result}',
                     reply_markup=get_buttons_for_message())


def get_buttons_for_message():
    yesButton = telebot.types.InlineKeyboardButton(text="Да", callback_data="In_yesButton")
    noButton = telebot.types.InlineKeyboardButton(text="Нет", callback_data="In_noButton")
    nextButton = telebot.types.InlineKeyboardButton(text="Следующий", callback_data="In_nextButton")
    return telebot.types.InlineKeyboardMarkup().add(yesButton, noButton, nextButton)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == 'In_yesButton':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text)
        db_service.add_question(call.message.text, 'COMPLETE', call.message.message_id)
    elif call.data == 'In_noButton':
        question_to_handle = gpt_service.handleMessageToQuestion(call.message.text)
        result = gpt_service.handleMessageToAnswer(neural_service.generate_answer(question_to_handle))
        bot.send_message(CHAT_ID, f'Вопрос: {question_to_handle}\n\nОтвет: {result}',
                         reply_markup=get_buttons_for_message())
    elif call.data == 'In_nextButton':
        db_service.add_question(call.message.text, 'WAIT', call.message.message_id)


# Запуск бота
if __name__ == '__main__':
    bot.infinity_polling()
