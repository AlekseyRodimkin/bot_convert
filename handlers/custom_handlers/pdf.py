from keyboards.reply.contact import pdf_to_target
from loader import bot
from states.states import UserState
from telebot.types import Message, ReplyKeyboardRemove
from Exeptions.exeptions_classes import FileFormatError
import os
from handlers.custom_handlers.algorithms import pdf_to_docx
from handlers.custom_handlers.errors import clearing_uploads, handle_error

uploads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))


@bot.message_handler(commands=["PDF"])
def pdf_to(message: Message) -> None:
    """
    Обработчик команды конвертации pdf.
    Переводит в состояние "Ожидание целевого формата".
    :param message: Полученное в чате сообщение
    :return
    """
    bot.send_message(message.from_user.id, f"🤖В какой формат конвертировать PDF файл",
                     reply_markup=(pdf_to_target()))
    bot.set_state(message.from_user.id, UserState.waiting_target_format, message.chat.id)


@bot.message_handler(state=UserState.waiting_target_format)
def waiting_target_format(message: Message) -> None:
    """
    Обработчик целевого формата
    Переводит в состояние "converting"
    Вызывает функцию запроса.
    :param message: Полученное в чате сообщение
    :return:
    """
    bot.send_message(message.from_user.id, f"🤖Пришлите файл", reply_markup=(ReplyKeyboardRemove()))
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
    src = os.path.join(uploads_path, message.document.file_name)
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    try:
        filename = message.document.file_name
        if not filename.endswith('pdf'):
            raise FileFormatError()
        bot.reply_to(message, "🤖Конвертирую...")
        src = os.path.join(uploads_path, message.document.file_name)
        new_filename = 'your_new_file.docx'

        if pdf_to_docx(src, new_filename):
            bot.send_document(message.chat.id, open(new_filename, 'rb'))
        else:
            handle_error(message, "Ошибка конвертирования")

    except FileFormatError as e:
        """Ошибка формата файла"""
        handle_error(message, "Не корректное расширение исходного файла")

    finally:
        bot.set_state(message.from_user.id, None, message.chat.id)
        clearing_uploads()
