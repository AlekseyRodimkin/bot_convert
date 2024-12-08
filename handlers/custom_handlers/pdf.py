from loader import bot
from telebot.types import Message, ReplyKeyboardRemove
from utils.misc.algorithms import pdf_to_docx, pdf_to_audio
from handlers import error_handler
from config_data.config import uploads_path
from loguru import logger
import os
from handlers.handler_decorator import command_handler
from states.states import UserState


def save_uploaded_file(document, user_id: int) -> str or None:
    """Сохраняет загруженный файл и возвращает его путь."""
    try:
        file_info = bot.get_file(document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        user_path = os.path.join(uploads_path, str(user_id))
        os.makedirs(user_path, exist_ok=True)

        file_path = os.path.join(user_path, document.file_name)
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        logger.info(f'Файл {document.file_name} сохранён.')
        return file_path
    except Exception as e:
        logger.error(f"Ошибка сохранения файла: {e}")
        return None


@bot.message_handler(commands=["PDF"])
@command_handler()
def pdf_main(message: Message) -> None:
    """Обработчик команды PDF. Предлагает выбор формата."""
    logger.info(f'{message.from_user.id}: /PDF')
    bot.send_message(
        message.from_user.id,
        "🤖Доступные конвертации:\n"
        "/docx - PDF в Word документ\n"
        "/mp3 - PDF в аудиокнигу\n\n"
        "Поддерживаю только русский язык",
        reply_markup=ReplyKeyboardRemove()
    )
    bot.set_state(message.from_user.id, UserState.waiting_target_format, message.chat.id)


@bot.message_handler(state=UserState.waiting_target_format)
@command_handler(state_required=UserState.waiting_target_format)
def pdf_select_format(message: Message) -> None:
    """Сохранение выбранного формата и перевод в состояние ожидания файла."""
    logger.info(f'{message.from_user.id}: Выбранный формат - {message.text}')
    target_format = message.text.strip().lower()[1:]

    if target_format not in ["docx", "mp3"]:
        bot.reply_to(message, "Неверный формат. Выберите docx или mp3.")
        return

    bot.send_message(message.from_user.id, f"🤖Пришлите PDF-файл для конвертации в {target_format}.")
    bot.set_state(message.from_user.id, UserState.waiting_file_pdf, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["target_format"] = target_format


@bot.message_handler(content_types=["document"], state=UserState.waiting_file_pdf)
@command_handler(state_required=UserState.waiting_file_pdf)
def pdf_process_file(message: Message) -> None:
    """Конвертация PDF-файла в выбранный формат."""
    logger.info(f'{message.from_user.id}: Получен файл {message.document.file_name}')

    file_path = save_uploaded_file(message.document, message.from_user.id)
    if not file_path or not file_path.endswith(".pdf"):
        error_handler.main(message, "Файл не является PDF. Загрузите корректный файл.")
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_format = data.get("target_format")

    output_path = os.path.join(uploads_path, str(message.from_user.id), f"converted.{target_format}")
    conversion_function = {"docx": pdf_to_docx, "mp3": pdf_to_audio}.get(target_format)

    if not conversion_function:
        error_handler.main(message, "Не удалось определить функцию конвертации.")
        return

    bot.reply_to(message, "🤖Конвертирую файл...\n")
    if conversion_function(file_path, output_path):
        with open(output_path, 'rb') as file:
            bot.send_document(message.chat.id, file)
            logger.info(f'{message.from_user.id}: Файл конвертирован и отправлен.')
    else:
        error_handler.main(message, f"Ошибка конвертации в {target_format}.")
