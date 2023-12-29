import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('CHAT_TEST')
ADMIN_SECRET = os.getenv('ADMIN_SECRET')
GPT_URL = 'http://localhost:6677/api/process'
