from loader import bot
from states.states import UserState
from telebot.types import Message
import os
from utils.misc.algorithms import get_qr
from utils.misc import clear_uploads, error_handler
from loguru import logger


@bot.message_handler(commands=["QR"])
def main(message: Message) -> None:
    """
    Обработчик команды QR.
    Переводит в состояние "Ожидание qr текста".
    :param message: Полученное в чате сообщение (команда)
    :return
    """
    logger.info(f'{message.from_user.id}: /QR')

    bot.send_message(message.from_user.id, "🤖Введите текст")
    bot.set_state(message.from_user.id, UserState.waiting_qr_text, message.chat.id)


@bot.message_handler(state=UserState.waiting_qr_text)
def waiting_qr_text(message: Message) -> None:
    """
    Обработчик данных текста для генерации qr
    :param message: Полученное в чате сообщение
    :return:
    """
    logger.info(f'{message.from_user.id}: waiting_qr_text({message.text})')

    result = get_qr(message.text)
    if result:
        bot.send_photo(chat_id=message.chat.id, photo=result)
        bot.set_state(message.from_user.id, None, message.chat.id)
        clear_uploads.main(message.from_user.id)
    else:
        error_handler.main(message, "Ошибка генерации")
