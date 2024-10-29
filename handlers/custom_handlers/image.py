from loader import bot
from states.states import UserState
from telebot.types import Message
from Exeptions.exeptions_classes import FileFormatError
import os
from utils.misc.algorithms import get_monochrome, get_noise, remove_background, format_replace
from utils.misc import clear_uploads, error_handler
from config_data.config import uploads_path
from loguru import logger


def send_image_options(user_id: int):
    """
    Функция отправки команд
    :param user_id: int: ID пользователя
    """
    bot.send_message(user_id, "🤖Вот что я могу делать с изображениями:\n"
                              "\n/format - конвертация jpg в png\n"
                              "\n/back - удаление фона с изображения🔵\n"
                              "\n/noisy - добавление шума🔣\n"
                              "\n/monochrome - конвертирование в черно-белую палитру🔳")


def send_file(message, file_path: str):
    """
    Функция для отправки файла
    :param chat_id: int: ID чата
    :param file_path: str: путь к файлу
    :return: None
    """
    try:
        with open(file_path, 'rb') as file:
            bot.send_document(message.chat_id, file)
    except Exception as e:
        logger.error(f"send_file(file_path): {e}")
        error_handler.main(message.chat.id, 'Ошибка отправки изображения')




def process_image_command(command, save_path, new_file_path, message):
    """
    Функция выполнения команды над изображением
    :param command: str: команда
    :param save_path: str: путь к исходному изображению
    :param new_file_path: str: путь к конвертированному изображению
    :param message: Message: сообщение пользователя
    """
    if command == "monochrome" and get_monochrome(save_path, new_file_path):
        send_file(message, new_file_path)
    elif command == "noisy" and get_noise(save_path, new_file_path):
        send_file(message, new_file_path)
    elif command == "back" and remove_background(save_path, new_file_path):
        send_file(message, new_file_path)
    elif command == "format":
        result = format_replace(save_path)
        if result:
            with open(result, 'rb') as file:
                bot.send_document(message.chat.id, file)
        else:
            error_handler.main(message, "Ошибка конвертации")
    else:
        error_handler.main(message, "Неверное действие")


@bot.message_handler(commands=["IMAGE"])
def main(message: Message) -> None:
    """
    Обработчик команды IMAGE.
    Переводит в состояние "Ожидание действия".
    :param message: Полученное в чате сообщение (команда)
    """
    logger.info(f'{message.from_user.id}: /IMAGE')
    send_image_options(message.from_user.id)
    bot.set_state(message.from_user.id, UserState.waiting_action_image, message.chat.id)


@bot.message_handler(state=UserState.waiting_action_image)
def waiting_action_image(message: Message) -> None:
    """
    Обработчик целевого действия
    Переводит в состояние "Ожидание изображения".
    :param message: Полученное в чате сообщение
    """
    if message.text == '/start':
        bot.delete_state(message.from_user.id)
        bot.send_message(message.from_user.id, "Вы вышли из режима работы с изображениями")
        return

    logger.info(f'{message.from_user.id}: waiting_action_image({message.text})')

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["command"] = message.text[1:]
    logger.info(f'{message.from_user.id}: {message.text}')

    bot.send_message(message.from_user.id, f"🤖Пришлите изображение")
    bot.set_state(message.from_user.id, UserState.waiting_image, message.chat.id)


@bot.message_handler(content_types=['photo'], state=UserState.waiting_image)
def waiting_image(message: Message) -> None:
    """
    Обработчик изображения
    :param message: Полученное в чате сообщение
    """
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_name = file_info.file_path.split('/')[1]
    save_path = os.path.join(f'{uploads_path}/{message.from_user.id}', file_name)
    logger.info(f'{message.from_user.id}: waiting_image({file_name})')

    try:
        downloaded_file = bot.download_file(file_info.file_path)
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        logger.debug(f'{message.from_user.id}: {file_name}: saved')

        bot.reply_to(message, "🤖Конвертирую...")

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            command = data.get("command")
            new_file_path = os.path.join(uploads_path, str(message.from_user.id), f"{command}_{file_name}")
            process_image_command(command, save_path, new_file_path, message)

    except FileNotFoundError as e:
        logger.error(f'File not found error while saving file {file_name}: {e}')
        bot.reply_to(message, "❌ Ошибка при сохранении файла. Пожалуйста, попробуйте еще раз.")

    except Exception as e:
        logger.error(f'Error saving file {file_name}: {e}')
        bot.reply_to(message, "❌ Произошла ошибка. Пожалуйста, попробуйте позже.")

    finally:
        bot.set_state(message.from_user.id, None, message.chat.id)
        clear_uploads.main(message.from_user.id)
