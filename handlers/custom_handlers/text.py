from loader import bot
from states.states import UserState
from telebot.types import Message
import os
from utils.misc.algorithms import text_to_image, text_to_audio
from utils.misc import clear_uploads, error_handler
from loguru import logger
from io import BytesIO


def send_audio(message, audio: BytesIO):
    """
    Функция для отправки аудио
    :param message: Message: сообщение пользователя
    :param audio: BytesIO: байтовый поток с аудио
    :return: None
    """
    try:
        bot.send_audio(message.chat.id, audio, title='Аудио', performer='TTS')
    except Exception as e:
        logger.error(f"send_audio(): {e}")
        bot.reply_to(message, "❌ Ошибка отправки аудио.")



def send_text_options(user_id: int):
    """
    Функция отправки команд
    :param user_id: int: ID пользователя
    """
    bot.send_message(user_id, "🤖Вот что я могу делать с текстом:\n"
                              "\n/art - конвертация в изображение (латиница)\n"
                              "\n/audio - конвертирование в аудио")


def send_image(message, file: BytesIO):
    """
    Функция для отправки изображения.
    :param message: Message: сообщение пользователя
    :param file: BytesIO: байтовый поток с изображением
    :return: None
    """
    try:
        bot.send_photo(chat_id=message.chat.id, photo=file)
    except Exception as e:
        logger.error(f"send_image(): {e}")
        error_handler.main(message.chat.id, 'Ошибка отправки изображения')


def process_text_command(command, message: Message):
    """
    Функция выполнения команды над текстом.
    :param command: str: команда
    :param message: Message: сообщение пользователя
    """
    if command == "art":
        image = text_to_image(message.text)
        if not image:
            error_handler.main(message, "Ошибка создания изображения")
        send_image(message, image)

    elif command == "audio":
        audio = text_to_audio(message.text)
        if not audio:
            error_handler.main(message, "Ошибка создания аудио")
        send_audio(message, audio)

    else:
        error_handler.main(message, "Неверное действие")


@bot.message_handler(commands=["TEXT"])
def main(message: Message) -> None:
    """
    Обработчик команды TEXT.
    Переводит в состояние "Ожидание действия для текста".
    :param message: Полученное в чате сообщение (команда)
    """
    logger.info(f'{message.from_user.id}: /TEXT')
    send_text_options(message.from_user.id)
    bot.set_state(message.from_user.id, UserState.waiting_action_text, message.chat.id)


@bot.message_handler(state=UserState.waiting_action_text)
def waiting_action_text(message: Message) -> None:
    """
    Обработчик целевого действия
    Переводит в состояние "Ожидание текста".
    :param message: Полученное в чате сообщение
    """
    if message.text == '/start':
        bot.delete_state(message.from_user.id)
        bot.send_message(message.from_user.id, "Вы вышли из режима работы с текстом")
        return

    logger.info(f'{message.from_user.id}: waiting_action_text({message.text})')

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["command"] = message.text[1:]
    logger.info(f'{message.from_user.id}: {message.text}')

    bot.send_message(message.from_user.id, f"🤖Пришлите текст (латиница)")
    bot.set_state(message.from_user.id, UserState.waiting_text, message.chat.id)


@bot.message_handler(state=UserState.waiting_text)
def waiting_text(message: Message) -> None:
    """
    Обработчик текста
    :param message: Полученное в чате сообщение
    """
    logger.info(f'{message.from_user.id}: waiting_text(text)')
    try:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            command = data.get("command")
            process_text_command(command, message)
    except Exception as e:
        logger.error(f'Error: {e}')
        bot.reply_to(message, "❌ Произошла ошибка. Пожалуйста, попробуйте позже.")

    finally:
        bot.set_state(message.from_user.id, None, message.chat.id)
        clear_uploads.main(message.from_user.id)
