from loader import bot
from states.states import UserState
from telebot.types import Message
import os
from handlers.custom_handlers.algorithms import get_barcode
from handlers.custom_handlers.errors import clearing_uploads, handle_error

uploads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))


@bot.message_handler(commands=["BARCODE"])
def image(message: Message) -> None:
    """
    Обработчик команды конвертации BAR.
    Переводит в состояние "Ожидание цифр".
    :param message: Полученное в чате сообщение (команда)
    :return
    """
    bot.send_message(message.from_user.id, "🤖Введите 1️⃣2️⃣ цифр для генерации кода")
    bot.set_state(message.from_user.id, UserState.waiting_numbers, message.chat.id)


@bot.message_handler(state=UserState.waiting_numbers)
def waiting_action_image(message: Message) -> None:
    """
    Обработчик целевого действия
    :param message: Полученное в чате сообщение
    :return:
    """

    if not message.text.isdigit() or len(message.text) != 12:
        handle_error(message, "Для генерации штрих-кода необходимо 1️⃣2️⃣ цифр")

    barcode_path = os.path.join(uploads_path, 'barcode')
    if get_barcode(message.text, barcode_path):
        bot.send_document(message.chat.id, open(f'{barcode_path}.png', 'rb'))
        bot.set_state(message.from_user.id, None, message.chat.id)
        clearing_uploads()
    else:
        handle_error(message, "Ошибка генерации")
