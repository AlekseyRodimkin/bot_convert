from loader import bot
from telebot.types import Message
from utils.misc.algorithms import text_to_image, text_to_audio
from utils.misc import clear_uploads
from handlers import error_handler
from loguru import logger
from io import BytesIO
from handlers.handler_decorator import command_handler
from states.states import UserState

processors = {
    "art": (text_to_image, 'image'),
    "audio": (text_to_audio, 'audio')
}


def send_media(message, media: BytesIO, media_type: str):
    """Функция для отправки медиа (аудио или изображения)."""
    try:
        if media_type == 'audio':
            bot.send_audio(message.chat.id, media, title='Аудио', performer='Ваше')
        elif media_type == 'image':
            bot.send_photo(chat_id=message.chat.id, photo=media)
    except Exception as e:
        logger.error(f"send_media({media_type}): {e}")
        error_handler.main(message, f"❌ Ошибка отправки {media_type}.")


def send_text_options(user_id: int):
    """Функция отправки команд."""
    options_message = (
        "🤖 Вот что я могу делать с текстом:\n"
        "\n/art - конвертация в изображение (латиница)\n"
        "\n/audio - конвертирование в аудио"
    )
    bot.send_message(user_id, options_message)


def process_text_command(command, message: Message):
    """Функция выполнения команды над текстом."""
    if command in processors:
        converter, media_type = processors[command]
        media = converter(message.text)

        if not media:
            error_handler.main(message, f"Ошибка создания {media_type}.")
        else:
            send_media(message, media, media_type)
    else:
        error_handler.main(message, "Неверное действие")


@bot.message_handler(commands=["TEXT"])
@command_handler()
def text_main(message: Message) -> None:
    """Обработчик команды TEXT."""
    logger.info(f'{message.from_user.id}: /TEXT')
    send_text_options(message.from_user.id)
    bot.set_state(message.from_user.id, UserState.waiting_action_text, message.chat.id)


@bot.message_handler(state=UserState.waiting_action_text)
@command_handler(state_required=UserState.waiting_action_text)
def waiting_action_text(message: Message) -> None:
    """Обработчик целевого действия."""
    if not processors.get(message.text[1:]):
        bot.reply_to(message, "Неверная команда. Выберите из предложенного списка.")
        send_text_options(message.from_user.id)
        return

    logger.info(f'{message.from_user.id}: waiting_action_text({message.text})')
    bot.set_state(message.from_user.id, UserState.waiting_text, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["command"] = message.text[1:]
    bot.send_message(message.from_user.id, "🤖 Пришлите текст (латиница)")


@bot.message_handler(state=UserState.waiting_text)
@command_handler(state_required=UserState.waiting_text)
def text_working(message: Message) -> None:
    """Обработчик текста."""
    logger.info(f'{message.from_user.id}: {message.text}.')
    try:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            command = data.get("command")
            process_text_command(command, message)
    except Exception as e:
        logger.error(f'Error: {e}')
        bot.reply_to(message, "❌ Произошла ошибка. Пожалуйста, попробуйте позже.")
    finally:
        bot.set_state(message.from_user.id, None, message.chat.id)
        clear_uploads.main(message.from_user.id)
