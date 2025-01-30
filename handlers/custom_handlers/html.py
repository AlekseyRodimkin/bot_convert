import os
from loader import bot
from telebot.types import Message
from utils.misc.algorithms import get_html, is_valid_url
from handlers import error_handler
from config_data.config import uploads_path
from loguru import logger
from handlers.handler_decorator import command_handler
from states.states import UserState


@bot.message_handler(commands=["HTML"])
@command_handler()
def html_main(message: Message) -> None:
    """
    Обработчик команды HTML. Переводит в состояние ожидания ссылки.
    """
    logger.info(f'{message.from_user.id}: /HTML')
    bot.send_message(
        message.from_user.id,
        "🤖Пришлите ссылку для получения HTML-кода.\n\n"
        "❗❗❗️Перед открытием убедитесь, что страница не содержит вредоносного кода."
    )
    bot.set_state(message.from_user.id, UserState.waiting_link, message.chat.id)


@bot.message_handler(state=UserState.waiting_link)
@command_handler(state_required=UserState.waiting_link)
def html_get(message: Message) -> None:
    """
    Получение HTML-кода по ссылке и отправка файла пользователю.
    """
    if not is_valid_url(message.text):
        bot.reply_to(message, "Некорректная ссылка")
        return

    logger.info(f'{message.from_user.id}: Получена ссылка - {message.text}')
    url = message.text.strip()
    html_content = get_html(url)
    if not html_content:
        error_handler.main(message, "Не удалось получить HTML-код. Проверьте ссылку.")
        return

    user_path = os.path.join(uploads_path, str(message.from_user.id))
    os.makedirs(user_path, exist_ok=True)
    file_path = os.path.join(user_path, "page.html")

    try:
        with open(file_path, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)

        with open(file_path, 'rb') as file:
            bot.send_document(message.chat.id, file)
            logger.info(f'{message.from_user.id}: HTML-файл отправлен.')
    except IOError as e:
        logger.error(f"Ошибка при записи HTML в файл: {e}")
        error_handler.main(message, "Ошибка сохранения HTML-кода.")
