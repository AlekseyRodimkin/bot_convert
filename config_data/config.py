import os
from dotenv import load_dotenv, find_dotenv
from loguru import logger

logger.add('logs/debug.log', format="{time} {level}    {message}", level="ERROR")

if not find_dotenv():
    logger.error('.env -> ???')
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Помогите")
)
