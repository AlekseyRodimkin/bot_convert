from loader import bot
from states.states import UserState
from telebot.types import Message
import os
from handlers.custom_handlers.algorithms import delete_file, get_barcode
import time


uploads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))


@bot.message_handler(commands=["BAR"])
def image(message: Message) -> None:
    """
    Обработчик команды конвертации BAR.
    Переводит в состояние "Ожидание цифр".
    :param message: Полученное в чате сообщение (команда)
    :return
    """
    bot.send_message(message.from_user.id, "🤖Введите 12 цифр для генерации кода")
    bot.set_state(message.from_user.id, UserState.waiting_numbers, message.chat.id)


@bot.message_handler(state=UserState.waiting_numbers)
def waiting_action_image(message: Message) -> None:
    """
    Обработчик целевого действия
    :param message: Полученное в чате сообщение
    :return:
    """

    if not message.text.isdigit():
        bot.set_state(message.from_user.id, None, message.chat.id)
        bot.send_message(message.from_user.id, "🤖Для генерации штрих-кода необходимо 12 цифр🔢")
        return
    if len(message.text) != 12:
        bot.set_state(message.from_user.id, None, message.chat.id)
        bot.send_message(message.from_user.id, "🤖Количество цифр должно быть 12🔢")
        return 

    if get_barcode(message.text):
        barcode_filename = os.path.join(uploads_path, 'barcode.png')

        if os.path.exists(barcode_filename):
            with open(barcode_filename, 'rb') as barcode_file:
                bot.send_document(message.chat.id, open(f'{barcode_filename}', 'rb'))
        else:
            time.sleep(2)
            with open(barcode_filename, 'rb') as barcode_file:
                bot.send_document(message.chat.id, open(f'{barcode_filename}', 'rb'))

        bot.set_state(message.from_user.id, None,  message.chat.id)
        delete_file(f'{barcode_filename}')
    else:
        bot.set_state(message.from_user.id, None, message.chat.id)
        bot.send_message(message.from_user.id, "🤖Ошибка генерации штрих-кода🔧")
