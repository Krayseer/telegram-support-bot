import sqlite3


# Добавить в таблицу вопрос
def add_question(question, state, message_id):
    conn = sqlite3.connect('helper.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS QuestionsStatus (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT,
                    status TEXT,
                    message_id INTEGER
                    )''')
    conn.execute('INSERT INTO QuestionsStatus (question, status, message_id) VALUES (?, ?, ?)',
                 (question, state, message_id))
    conn.commit()
    conn.close()
