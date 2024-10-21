from keyboards.reply.contact import pdf_to_target
from loader import bot
from states.states import UserState
from telebot.types import Message, ReplyKeyboardRemove
from Exeptions.exeptions_classes import FileFormatError
import os
from handlers.custom_handlers.algorithms import pdf_to_docx, pdf_to_book
from handlers.custom_handlers.errors import clearing_uploads, handle_error

uploads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))

FORMAT_ACTIONS = {
    'docx': pdf_to_docx,
    'mp3': pdf_to_book
}


@bot.message_handler(commands=["PDF"])
def pdf_to(message: Message) -> None:
    """
    Обработчик команды конвертации pdf.
    Переводит в состояние "Ожидание целевого формата".
    """
    bot.send_message(
        message.from_user.id,
        "docx - конвертация в word документ\n"
        "mp3 - конвертация в аудио книгу\n"
        "\nВ какой формат конвертировать PDF файл",
        reply_markup=pdf_to_target()
    )
    bot.set_state(message.from_user.id, UserState.waiting_target_format, message.chat.id)


@bot.message_handler(state=UserState.waiting_target_format)
def waiting_target_format(message: Message) -> None:
    """
    Обработчик целевого формата.
    Переводит в состояние "Ожидание файла" и сохраняет выбранный формат.
    """
    target_format = message.text[1:]
    if target_format not in FORMAT_ACTIONS:
        return handle_error(message, "Неверный формат. Пожалуйста, выберите PDF или MP3.")

    bot.send_message(
        message.from_user.id,
        f"🤖Пришлите файл для конвертации в {target_format}",
        reply_markup=ReplyKeyboardRemove()
    )
    bot.set_state(message.from_user.id, UserState.waiting_file_pdf, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["user_id"] = message.from_user.id
        data["target_format"] = target_format


@bot.message_handler(content_types=['document'], state=UserState.waiting_file_pdf)
def handle_docs_photo(message: Message) -> None:
    """
    Обработчик файла.
    Конвертирует файл в выбранный формат.
    """
    try:
        src = save_downloaded_file(message.document)
        user_id = message.from_user.id
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            target_format = data.get('target_format')

        if not validate_file_format(message.document.file_name):
            raise FileFormatError()

        bot.reply_to(message, "🤖Конвертирую...")
        new_filename = os.path.join(uploads_path, f'your_new_file.{target_format}')
        conversion_function = FORMAT_ACTIONS.get(target_format)

        if conversion_function(src, new_filename):
            bot.send_document(message.chat.id, open(new_filename, 'rb'))
        else:
            handle_error(message, "Ошибка конвертирования")

    except FileFormatError:
        handle_error(message, "Не корректное расширение исходного файла")

    finally:
        bot.set_state(message.from_user.id, None, message.chat.id)
        clearing_uploads()


def save_downloaded_file(document) -> str:
    """
    Сохраняет загруженный файл на сервере.
    """
    file_info = bot.get_file(document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = os.path.join(uploads_path, document.file_name)

    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    return src


def validate_file_format(filename: str) -> bool:
    """
    Проверяет, что файл имеет корректный формат.
    """
    return filename.endswith('pdf')
