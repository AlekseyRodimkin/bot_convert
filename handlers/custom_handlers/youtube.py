from loader import bot
from telebot.types import Message
from utils.misc import clear_uploads
from utils.misc.algorithms import is_valid_url
from utils.misc import youtube
from loguru import logger
from handlers.handler_decorator import command_handler
from states.states import UserState
import os
import subprocess
from config_data.config import uploads_path
from .. import error_handler


def send_video_options(user_id: int):
    """Функция отправки команд."""
    options_message = (
        "🤖 Выберите качество для файла:\n"
        "\n/yandex - сохранить на Яндекс Диск и прислать ссылку\n"
    )
    bot.send_message(user_id, options_message)


@bot.message_handler(commands=["YTB"])
@command_handler()
def main_youtube(message: Message) -> None:
    """Обработчик команды YTB."""
    logger.info(f'{message.from_user.id}: /YTB')
    send_video_options(message.from_user.id)
    bot.set_state(message.from_user.id, UserState.waiting_resolution, message.chat.id)


@bot.message_handler(state=UserState.waiting_resolution)
@command_handler(state_required=UserState.waiting_resolution)
def res_youtube(message: Message) -> None:
    """Обработчик качества видео."""
    if message.text not in ("/yandex"):
        send_video_options(message.from_user.id)
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["target_place"] = message.text[1:]
    logger.info(f'{message.from_user.id}: get_link({message.text})')

    bot.send_message(message.from_user.id, f"🤖Пришлите сылку на видео youtube")
    bot.set_state(message.from_user.id, UserState.waiting_video_link, message.chat.id)


@bot.message_handler(state=UserState.waiting_video_link)
@command_handler(state_required=UserState.waiting_video_link)
def get_video(message: Message) -> None:
    """Обработчик ссылки """
    if not is_valid_url(message.text):
        bot.reply_to(message, "Некорректная ссылка")
        return

    logger.info(f'{message.from_user.id}: get_video({message.text})')
    bot.send_message(message.from_user.id, f"🤖Начинаю скачивание, пришлю как закончу...")
    try:
        path = os.path.join(uploads_path, str(message.from_user.id))

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            result = youtube.main(
                user_upl_path=path,
                link=message.text
            )
            bot.send_message(message.from_user.id, f"🤖 Ссылка на файл в Яндекс диске\n{result}")

    except Exception as e:
        error_handler.main(message, "Произошла ошибка, попробуйте позже", e)
    finally:
        bot.set_state(message.from_user.id, None, message.chat.id)
        clear_uploads.main(message.from_user.id)
