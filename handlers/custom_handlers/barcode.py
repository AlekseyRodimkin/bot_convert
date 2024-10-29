from loader import bot
from states.states import UserState
from telebot.types import Message
import os
from utils.misc.algorithms import get_barcode
from utils.misc import clear_uploads, error_handler
from config_data.config import uploads_path
from loguru import logger


@bot.message_handler(commands=["BARCODE"])
def main(message: Message) -> None:
    """
    Обработчик команды BARCODE.
    Переводит в состояние "Ожидание цифр".
    :param message: Полученное в чате сообщение (команда)
    """
    logger.info(f'{message.from_user.id}: /BARCODE')

    bot.send_message(message.from_user.id, "🤖Введите 1️⃣2️⃣ цифр для генерации кода")
    bot.set_state(message.from_user.id, UserState.waiting_numbers, message.chat.id)


@bot.message_handler(state=UserState.waiting_numbers)
def waiting_numbers(message: Message) -> None:
    """
    Обработчик целевого действия
    :param message: Полученное в чате сообщение
    """
    logger.info(f'{message.from_user.id}: waiting_numbers({message.text})')

    if not message.text.isdigit() or len(message.text) != 12:
        error_handler.main(message, "Для генерации штрих-кода необходимо 1️⃣2️⃣ цифр")
        return

    barcode_path = os.path.join(f'{uploads_path}/{message.from_user.id}', 'barcode')
    if get_barcode(message.text, barcode_path):
        bot.send_document(message.chat.id, open(f'{barcode_path}.png', 'rb'))
        logger.info(f'send_document: {message.from_user.id}: barcode.png')
        bot.set_state(message.from_user.id, None, message.chat.id)
        clear_uploads.main(message.from_user.id)
    else:
        error_handler.main(message, "Ошибка генерации")
