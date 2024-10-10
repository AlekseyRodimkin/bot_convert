from keyboards.reply.contact import pdf_to_target
from loader import bot
from states.states import UserState
from telebot.types import Message, ReplyKeyboardRemove
from Exeptions.exeptions_classes import FileFormatError
import os
from handlers.custom_handlers.algorithms import pdf_to_docx, delete_file

basedir = os.path.abspath(os.path.dirname(__file__))


@bot.message_handler(commands=["PDF"])
def pdf_to(message: Message) -> None:
    """
    Обработчик команды конвертации pdf.
    Переводит в состояние "Ожидание целевого формата".
    :param message: Полученное в чате сообщение
    :return
    """
    bot.send_message(message.from_user.id, f"В какой формат конвертировать PDF файл",
                     reply_markup=(pdf_to_target()))
    bot.set_state(message.from_user.id, UserState.waiting_target_format, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["command"] = message.text
        data["user_id"] = message.from_user.id
        data["format"] = '.' + message.text.lower()[1:]


@bot.message_handler(state=UserState.waiting_target_format)
def waiting_target_format(message: Message) -> None:
    """
    Обработчик целевого формата
    Переводит в состояние "converting"
    Вызывает функцию запроса.
    :param message: Полученное в чате сообщение
    :return:
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["to"] = '.' + message.text.lower()[1:]

    bot.send_message(message.from_user.id, f"Пришлите файл", reply_markup=(ReplyKeyboardRemove()))
    bot.set_state(message.from_user.id, UserState.waiting_file_pdf, message.chat.id)


@bot.message_handler(content_types=['document'], state=UserState.waiting_file_pdf)
def handle_docs_photo(message: Message) -> None:
    """
    Обработчик файла
    Переводит в состояние "converting"
    :param message: Полученное в чате сообщение
    :return:
    """
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
            bot.reply_to(message, "Конвертирую...")
            src = os.path.join(basedir, '../../uploads', message.document.file_name)
            new_filename = filename.split('.')[0] + data['to']

            if pdf_to_docx(src, new_filename):
                bot.send_document(message.chat.id, open(new_filename, 'rb'))
                delete_file(new_filename)
                delete_file(src)
                bot.set_state(message.from_user.id, None, message.chat.id)
                return
            else:
                bot.send_message(message.chat.id,
                                 "Ошибка конвертирования, попробуйте еще раз или сообщите о проблеме по команде /help")
                bot.set_state(message.from_user.id, None, message.chat.id)
                delete_file(src)
                return

    except FileFormatError:
        """Ошибка формата файла"""
        delete_file(src)
        bot.set_state(message.from_user.id, None, message.chat.id)
        bot.send_message(message.from_user.id,
                         f"Не корректное расширение исходного файла, нажмите /start чтобы получить список команд")
        return
