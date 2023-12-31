messages_dict = {
    'start.bot': 'Техническая поддержка запущена',

    'redirect.admin': 'Перенаправляем ваш запрос на администратора',

    'message.to-question': 'Сделай из этого сообщения адекватный вопрос, и выдай мне только полученный вопрос, '
                           'без всего лишнего: ',
    'message.to-answer': 'Можешь исходя из этого вопроса из этого текста составить ответ, но не меняя смысла и логики: ',

    'admin.already-exists': 'Вы уже являетесь администратором',

    'login.success': 'Вы успешно авторизованы как администратор',
    'login.invalid.secret-key': 'Неверный секретный ключ',
    'login.invalid.format': 'Используйте команду в формате /login <секретный_ключ>',

    'logout.success': 'Вы потеряли права администратора',
    'logout.error': 'Вы не являетесь администратором',

    'commons.yes': 'Да',
    'commons.no': 'Нет',
    'commons.to-admin': 'В тех-поддержку'
}


# Получить сообщение по ключу
def get_message_by_key(key):
    return messages_dict.get(key, 'Сообщение не найдено')
