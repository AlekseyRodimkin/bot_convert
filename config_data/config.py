import os
from dotenv import load_dotenv, find_dotenv
from loguru import logger

if not find_dotenv():
    logger.error('.env is missing')
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

uploads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../uploads'))
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEFAULT_COMMANDS = (
    ('start', "Список команд"),
    ('help', "Помогите")
)
