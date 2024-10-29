from loader import bot
from states.states import UserState
from telebot.types import Message
import os
from utils.misc.algorithms import get_html
from config_data.config import uploads_path
from utils.misc import clear_uploads, error_handler
from loguru import logger


@bot.message_handler(commands=["HTML"])
def main(message: Message) -> None:
    """
    Обработчик команды HTML.
    Переводит в состояние "Ожидание ссылки".
    :param message: Полученное в чате сообщение (команда)
    """
    logger.info(f'{message.from_user.id}: /HTML')

    bot.send_message(message.from_user.id,
                     "🤖Пришлите ссылку\n"
                     "\n❗❗❗️Перед открытием документа убедитесь в отсутствии вредоносного кода или XSS❗❗❗")
    bot.set_state(message.from_user.id, UserState.waiting_link, message.chat.id)


@bot.message_handler(state=UserState.waiting_link)
def waiting_link(message: Message) -> None:
    """
    Обработчик ссылки
    :param message: Полученное в чате сообщение
    """
    logger.info(f'{message.from_user.id}: waiting_link({message.text})')

    url = message.text
    html_content = get_html(url)
    if html_content:
        file_path = os.path.join(f'{uploads_path}/{message.from_user.id}', 'your_code.html')
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            logger.debug(f'waiting_link({url}) : saved')
        except IOError:
            error_handler.main(message, "Ошибка сохранения файла")
        with open(file_path, 'rb') as file:
            bot.send_document(message.chat.id, file)
        logger.info(f'send_document: {message.from_user.id}: your_code.html')
        bot.set_state(message.from_user.id, None, message.chat.id)
        clear_uploads.main(message.from_user.id)

    else:
        error_handler.main(message, "Не удалось сохранить страницу")
