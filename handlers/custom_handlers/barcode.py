from loader import bot
from telebot.types import Message
from utils.misc.algorithms import get_barcode
from handlers import error_handler
from config_data.config import uploads_path
from loguru import logger
import os
from handlers.handler_decorator import command_handler
from states.states import UserState
from utils.misc import clear_uploads


@bot.message_handler(commands=["BARCODE"])
@command_handler()
def barcode_main(message: Message) -> None:
    """Обработчик команды BARCODE. Переводит в состояние "Ожидание цифр"."""
    logger.info(f'{message.from_user.id}: /BARCODE')
    bot.send_message(message.from_user.id, "🤖Введите 1️⃣2️⃣ цифр для генерации кода")
    bot.set_state(message.from_user.id, UserState.waiting_numbers, message.chat.id)


@bot.message_handler(state=UserState.waiting_numbers)
@command_handler(state_required=UserState.waiting_numbers)
def barcode_generate(message: Message) -> None:
    """Обработка 12-значного числа и генерация штрих-кода."""
    if not message.text.isdigit() or len(message.text) != 12:
        bot.reply_to(message, "Для генерации штрих-кода необходимо 1️⃣2️⃣ цифр")
        return

    logger.info(f'{message.from_user.id}: waiting_numbers({message.text})')
    barcode_path = os.path.join(uploads_path, str(message.from_user.id), message.text)
    if get_barcode(message.text, barcode_path):
        bot.send_document(message.chat.id, open(f'{barcode_path}.png', 'rb'))
        logger.info(f'Штрих-код отправлен: {message.from_user.id}')
        clear_uploads.main(message.from_user.id)
    else:
        error_handler.main(message, "Ошибка генерации штрих-кода")
