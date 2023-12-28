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


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    question = message.text
    question_to_handle = gpt_service.handleMessageToQuestion(question)
    result = gpt_service.handleMessageToAnswer(neural_service.generate_answer(question_to_handle))
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
        question_to_handle = gpt_service.handleMessageToQuestion(question)
        result = gpt_service.handleMessageToAnswer(neural_service.generate_answer(question_to_handle))
        buttons = create_inline_keyboard(question)
        bot.edit_message_text(chat_id=CHAT_ID, message_id=call.message.message_id,
                              text=f'Вопрос: {question}\n\nОтвет: {result}', reply_markup=buttons)

    elif name == 'TO_ADMIN':
        db_service.add_question(question, 'WAIT', call.message.message_id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Вопрос: {question}\n\nОжидается ответ администратора...')


if __name__ == '__main__':
    bot.infinity_polling()
