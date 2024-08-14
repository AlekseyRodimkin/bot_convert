from keyboards.reply.contact import pdf_to_target
from loader import bot
from states.contact_information import UserInfoState
from telebot.types import Message, ReplyKeyboardRemove
from loguru import logger
from Exeptions.exeptions_classes import FileFormatError
import os
from handlers.custom_handlers.algorithms import pdf_to_docx, delete_docs
basedir = os.path.abspath(os.path.dirname(__file__))


@bot.message_handler(commands=["PDF"])
def pdf_to(message: Message) -> None:
    """
    Обработчик команды конвертации pdf.
    Переводит в состояние "Ожидание целевого формата".
    :param message: Полученное в чате сообщение (команда)
    :return
    """
    bot.send_message(message.from_user.id, f"В какой формат конвертировать PDF файл",
                     reply_markup=(pdf_to_target()))
    bot.set_state(message.from_user.id, UserInfoState.waiting_target_format, message.chat.id)
    logger.debug("func -> pdf_to")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["command"] = message.text
        data["user_id"] = message.from_user.id
        data["format"] = '.' + message.text.lower()[1:]
        logger.debug(f"bot.retrieve_data -> data['command'] = {data['command']}")
        logger.debug(f"bot.retrieve_data -> data['user_id'] = {message.from_user.id}")
        logger.debug(f"bot.retrieve_data -> data['format']'] = {data['format']}")


@bot.message_handler(state=UserInfoState.waiting_target_format)
def waiting_target_format(message: Message) -> None:
    """
    Обработчик целевого формата
    Переводит в состояние "converting"
    Вызывает функцию запроса.
    :param message: Полученное в чате сообщение (город)
    :return:
    """
    logger.debug("func -> waiting_target_format")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["to"] = '.' + message.text.lower()[1:]
        logger.debug(f"bot.retrieve_data -> data['to'] = {data['to']}")

    bot.send_message(message.from_user.id, f"Пришлите файл", reply_markup=(ReplyKeyboardRemove()))
    bot.set_state(message.from_user.id, UserInfoState.waiting_file, message.chat.id)


@bot.message_handler(content_types=['document'], state=UserInfoState.waiting_file)
def handle_docs_photo(message: Message) -> None:
    """
    Обработчик файла
    Переводит в состояние "converting"
    :param message: Полученное в чате сообщение (город)
    :return:
    """
    logger.debug("func -> handle_docs_photo")
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = os.path.join(basedir, '../../uploads', message.document.file_name)
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    try:
        filename = message.document.file_name
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if not filename.endswith(data['format']):
                raise FileFormatError()
            bot.reply_to(message, "Расширение проверено, работаю")
            src = os.path.join(basedir, '../../uploads', message.document.file_name)
            new_filename = filename.split('.')[0] + data['to']
            pdf_to_docx(src, new_filename)
        bot.send_document(message.chat.id, open(new_filename, 'rb'))
        delete_docs(new_filename)
        delete_docs(src)
        bot.set_state(message.from_user.id, None, message.chat.id)
        return


    except FileFormatError:
        """Ошибка формата файла"""
        bot.set_state(message.from_user.id, None, message.chat.id)
        logger.debug("File format error")
        logger.debug("State -> None")
        bot.send_message(message.from_user.id, f"Не корректное расширение исходного файла, повторите командой /start",
                         reply_markup=(ReplyKeyboardRemove()))
        return
