# Класс, хранящий информацию сообщениях бота
class MessageProvider:
    messages_dict = {
        'start.bot': 'Техническая поддержка запущена',
        'redirect.admin': 'Перенаправляем ваш запрос на администратора'
    }

    # Получить сообщение по ключу
    def get_message_by_key(self, key):
        return self.messages_dict.get(key, 'Сообщение не найдено')
