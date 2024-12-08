from loader import bot
from telebot.types import Message
from utils.misc.algorithms import get_qr
from utils.misc import clear_uploads
from handlers import error_handler
from loguru import logger
from handlers.handler_decorator import command_handler
from states.states import UserState


@bot.message_handler(commands=["QR"])
@command_handler()
def qr_main(message: Message) -> None:
    """Обработчик команды QR."""
    logger.info(f'{message.from_user.id}: /QR')

    bot.send_message(message.from_user.id, "🤖Введите текст")
    bot.set_state(message.from_user.id, UserState.waiting_qr_text, message.chat.id)


@bot.message_handler(state=UserState.waiting_qr_text)
@command_handler(state_required=UserState.waiting_qr_text)
def get_qr_image(message: Message) -> None:
    """Обработчик данных для генерации qr"""
    logger.info(f'{message.from_user.id}: {message.text}.')
    result = get_qr(message.text)
    if result:
        bot.send_photo(chat_id=message.chat.id, photo=result)
        bot.set_state(message.from_user.id, None, message.chat.id)
        clear_uploads.main(message.from_user.id)
    else:
        error_handler.main(message, "Ошибка генерации")
