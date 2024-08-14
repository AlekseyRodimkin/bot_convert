from config_data.config import DEFAULT_COMMANDS
from loader import bot
from loguru import logger
from telebot.types import Message, ReplyKeyboardRemove

logger.add('logs/debug.log', format="{time} {level}    {message}", level="DEBUG")


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    """
    Обработчик команды <help>.
    Выводит список команд.
    :param message: Полученное в чате сообщение
    :return:
    """
    logger.debug("/help")
    text = f'Telegram: https://t.me/mr_dagestan\nEmail: alexeyrodimkin@gmail.com'
    bot.reply_to(message, text, reply_markup=(ReplyKeyboardRemove()))
