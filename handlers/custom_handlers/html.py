from loader import bot
from states.states import UserState
from telebot.types import Message
import os
from handlers.custom_handlers.algorithms import get_html
from handlers.custom_handlers.errors import clearing_uploads, handle_error


uploads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))


@bot.message_handler(commands=["HTML"])
def index(message: Message) -> None:
    """
    Обработчик команды конвертации HTML.
    Переводит в состояние "Ожидание ссылки".
    :param message: Полученное в чате сообщение (команда)
    :return
    """
    bot.send_message(message.from_user.id,
                     "🤖Пришлите ссылку\n"
                     "\n❗❗❗️Перед открытием документа убедитесь в отсутствии вредоносного кода или XSS❗❗❗")
    bot.set_state(message.from_user.id, UserState.waiting_link, message.chat.id)


@bot.message_handler(state=UserState.waiting_link)
def waiting_link(message: Message) -> None:
    """
    Обработчик ссылки
    :param message: Полученное в чате сообщение
    :return:
    """
    url = message.text
    html_content = get_html(url)
    if html_content:
        file_path = os.path.join(uploads_path, 'your_code.html')
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
        except IOError as e:
            handle_error(message, "Ошибка сохранения файла")
        with open(file_path, 'rb') as file:
            bot.send_document(message.chat.id, file)
        bot.set_state(message.from_user.id, None, message.chat.id)
        clearing_uploads()

    else:
        handle_error(message, "Не удалось сохранить страницу")
