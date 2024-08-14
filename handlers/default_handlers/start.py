from telebot.types import Message
from keyboards.reply.contact import start_buttons
from loader import bot
from loguru import logger
from states.contact_information import UserInfoState

logger.add('logs/debug.log', format="{time} {level}    {message}", level="DEBUG")


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    """
    Обработчик команды <start>.
    Выводит приветствие по имени пользователя.
    Выводит таблицу команд.
    :param message: Полученное в чате сообщение
    :return:
    """
    logger.debug("/start")
    bot.send_message(message.from_user.id, f'Приветствую {message.from_user.first_name}\n'
                                           f'Что вы хотите конвертировать',
                     reply_markup=start_buttons())
