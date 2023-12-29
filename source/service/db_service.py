import sqlite3


# Добавить в таблицу вопрос
def add_question(question, state, message_id):
    # Используем контекстный менеджер для автоматического закрытия соединения
    with sqlite3.connect('helper.db') as conn:
        # Создаем курсор
        cursor = conn.cursor()

        # Создаем таблицу, если её нет
        cursor.execute('''CREATE TABLE IF NOT EXISTS QuestionsStatus (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            question TEXT,
                            status TEXT,
                            message_id INTEGER
                            )''')

        # Вставляем данные
        cursor.execute('INSERT INTO QuestionsStatus (question, status, message_id) VALUES (?, ?, ?)',
                       (question, state, message_id))

        # Фиксируем изменения
        conn.commit()


# Добавить в таблицу админа по ID
def add_admin(user_id):
    with sqlite3.connect('helper.db') as conn:
        cursor = conn.cursor()

        # Создаем таблицу, если её нет
        cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
                            admin_id INTEGER PRIMARY KEY
                        )''')

        # Добавление администратора, игнорируя, если уже существует
        cursor.execute('INSERT OR IGNORE INTO admins (admin_id) VALUES (?)', (user_id,))

        # Фиксируем изменения
        conn.commit()


# Удалить админа из таблицы по ID
def remove_admin(user_id):
    with sqlite3.connect('helper.db') as conn:
        cursor = conn.cursor()

        # Удаление администратора из таблицы по ID
        cursor.execute('DELETE FROM admins WHERE admin_id = ?', (user_id,))

        # Фиксируем изменения
        conn.commit()


# Проверить, является ли пользователь админом
def is_admin(user_id):
    conn = sqlite3.connect('helper.db')
    cursor = conn.cursor()

    # Проверка, является ли пользователь администратором
    cursor.execute('SELECT * FROM admins WHERE admin_id = ?', (user_id,))
    result = cursor.fetchone()

    conn.close()

    return result is not None


# Получить все необработанные заявки
def get_WAIT_requests():
    with sqlite3.connect('helper.db') as conn:
        cursor = conn.cursor()

        # Выполняем запрос к таблице QuestionsStatus для получения всех заявок со статусом WAIT
        cursor.execute('SELECT * FROM QuestionsStatus WHERE status = ?', ('WAIT',))

        # Получаем все строки (заявки) из результата запроса
        waiting_requests = cursor.fetchall()

        # Возвращаем список заявок со статусом WAIT
        return waiting_requests


# Изменить статус заявки
def update_request_status(request_id):
    with sqlite3.connect('helper.db') as conn:
        cursor = conn.cursor()

        # Выполняем запрос на обновление статуса заявки
        cursor.execute('UPDATE QuestionsStatus SET status = ? WHERE id = ?', ('COMPLETE', request_id))

        # Фиксируем изменения
        conn.commit()


# Добавить состояние чата
def add_chat_state(user_id, request_id):
    with sqlite3.connect('helper.db') as conn:
        cursor = conn.cursor()

        # Создаем таблицу, если её нет
        cursor.execute('''CREATE TABLE IF NOT EXISTS ChatStates (
                            chat_id INTEGER PRIMARY KEY,
                            request_id INTEGER,
                            admin_response TEXT
                        )''')

        # Добавляем данные
        cursor.execute('INSERT OR REPLACE INTO ChatStates (chat_id, request_id) VALUES (?, ?)',
                       (user_id, request_id))

        # Фиксируем изменения
        conn.commit()


# Получить состояние чата
def get_chat_state(user_id):
    with sqlite3.connect('helper.db') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM ChatStates WHERE chat_id = ?', (user_id,))
        result = cursor.fetchone()

        return result


# Удалить состояние чата
def remove_chat_state(user_id):
    with sqlite3.connect('helper.db') as conn:
        cursor = conn.cursor()

        cursor.execute('DELETE FROM ChatStates WHERE chat_id = ?', (user_id,))

        conn.commit()


# Поиск заявки по id
def find_question_by_id(question_id):
    # Используем контекстный менеджер для автоматического закрытия соединения
    with sqlite3.connect('helper.db') as conn:
        cursor = conn.cursor()

        # Выполняем SQL-запрос для поиска заявки по ID
        cursor.execute('SELECT * FROM QuestionsStatus WHERE id = ?', (question_id,))

        # Получаем результат запроса
        question = cursor.fetchone()

        return question
