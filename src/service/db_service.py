import sqlite3

name = '../helper.db'


# Добавить в таблицу вопрос
def add_question(question, state, message_id):
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS QuestionsStatus (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            question TEXT,
                            status TEXT,
                            message_id INTEGER
                            )''')
        cursor.execute('INSERT INTO QuestionsStatus (question, status, message_id) VALUES (?, ?, ?)',
                       (question, state, message_id))
        conn.commit()


# Добавить в таблицу админа по ID
def add_admin(user_id):
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
                            admin_id INTEGER PRIMARY KEY
                        )''')
        cursor.execute('INSERT OR IGNORE INTO admins (admin_id) VALUES (?)', (user_id,))
        conn.commit()


# Удалить админа из таблицы по ID
def remove_admin(user_id):
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM admins WHERE admin_id = ?', (user_id,))
        conn.commit()


# Проверить, является ли пользователь админом
def is_admin(user_id):
    conn = sqlite3.connect(name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admins WHERE admin_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


# Получить все необработанные заявки
def get_WAIT_requests():
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM QuestionsStatus WHERE status = ?', ('WAIT',))
        waiting_requests = cursor.fetchall()
        return waiting_requests


# Изменить статус заявки
def update_request_status(request_id):
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE QuestionsStatus SET status = ? WHERE message_id = ?', ('COMPLETE', request_id))
        conn.commit()


# Добавить состояние чата
def add_chat_state(chat_id, question_text):
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS ChatStates (
                            chat_id INTEGER PRIMARY KEY,
                            question_text TEXT,
                            admin_response TEXT
                        )''')
        cursor.execute('INSERT OR REPLACE INTO ChatStates (chat_id, question_text) VALUES (?, ?)',
                       (chat_id, question_text))
        conn.commit()


def find_question_by_text(question_text):
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM QuestionsStatus WHERE question = ?', (question_text,))
        question = cursor.fetchone()
        return question[3]


# Получить состояние чата
def get_chat_state(chat_id):
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ChatStates WHERE chat_id = ?', (chat_id,))
        result = cursor.fetchone()
        return result


# Удалить состояние чата
def remove_chat_state(chat_id):
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM ChatStates WHERE chat_id = ?', (chat_id,))
        conn.commit()


# Поиск заявки по id
def find_question_by_id(question_id):
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM QuestionsStatus WHERE id = ?', (question_id,))
        return cursor.fetchone()
