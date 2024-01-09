import sqlite3

name = '../helper.db'


# Создать таблицы в БД, если они не существуют
def create_tables_for_db():
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
                            admin_id INTEGER PRIMARY KEY
                        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS QuestionsStatus (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                question TEXT,
                                status TEXT,
                                message_id INTEGER
                            )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS ChatStates (
                                    chat_id INTEGER PRIMARY KEY,
                                    question_text TEXT,
                                    admin_response TEXT
                            )''')
        conn.commit()


# Добавить в таблицу вопрос
def add_question(question, state, message_id):
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO QuestionsStatus (question, status, message_id) VALUES (?, ?, ?)',
                       (question, state, message_id))
        conn.commit()


# Добавить в таблицу админа по ID
def add_admin(chat_id):
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO admins (admin_id) VALUES (?)', (chat_id,))
        conn.commit()


# Удалить админа из таблицы по ID
def remove_admin(chat_id):
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM admins WHERE admin_id = ?', (chat_id,))
        conn.commit()


# Проверить, является ли пользователь админом
def is_user_admin(chat_id):
    conn = sqlite3.connect(name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admins WHERE admin_id = ?', (chat_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


# Получить все необработанные заявки
def get_all_tasks():
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM QuestionsStatus WHERE status = ?', ('WAIT',))
        return cursor.fetchall()


# Изменить статус заявки
def update_request_status(request_id):
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE QuestionsStatus SET status = ? WHERE message_id = ?', ('COMPLETE', request_id))
        conn.commit()


def find_question_by_text(question_text):
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM QuestionsStatus WHERE question = ?', (question_text,))
        return cursor.fetchone()[3]


# Добавить состояние чата
def add_chat_state(chat_id, question_text):
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO ChatStates (chat_id, question_text) VALUES (?, ?)',
                       (chat_id, question_text))
        conn.commit()


# Получить состояние чата
def get_chat_state(chat_id):
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ChatStates WHERE chat_id = ?', (chat_id,))
        return cursor.fetchone()


# Удалить состояние чата
def remove_chat_state(chat_id):
    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM ChatStates WHERE chat_id = ?', (chat_id,))
        conn.commit()
