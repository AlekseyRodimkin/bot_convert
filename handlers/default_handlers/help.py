from config_data.config import DEFAULT_COMMANDS
from loader import bot
from telebot.types import Message, ReplyKeyboardRemove


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    """
    Обработчик команды <help>.
    Выводит список команд.
    :param message: Полученное в чате сообщение
    :return:
    """
    text = f'Telegram: https://t.me/mr_dagestan\nEmail: alexeyrodimkin@gmail.com'
    bot.reply_to(message, text, reply_markup=(ReplyKeyboardRemove()))
