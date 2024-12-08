import os
from loader import bot
from telebot.types import ReplyKeyboardRemove
from utils.misc import clear_uploads
from loguru import logger


def main(message, error_code, log = '') -> None:
    """
    Обработчик ошибок.
    Удаляет папку uploads/<user_id>
    Переводит в состояние None
    :param message: Полученное в чате сообщение
    :param error_code: Сообщение ошибки
    :param log: Сообщение для логирования
    """
    clear_uploads.main(message.from_user.id)
    bot.set_state(message.from_user.id, None, message.chat.id)
    bot.send_message(message.chat.id,
                     f"‼️Ошибка ({error_code})‼️", reply_markup=ReplyKeyboardRemove())
    logger.error(f'{message.from_user.id}: {error_code}: {log}')
