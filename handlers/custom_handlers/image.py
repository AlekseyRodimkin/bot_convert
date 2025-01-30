from loader import bot
from telebot.types import Message
from utils.misc.algorithms import get_monochrome, get_noise, format_replace
from handlers import error_handler
from config_data.config import uploads_path
from loguru import logger
import os
from handlers.handler_decorator import command_handler
from states.states import UserState
from utils.misc import clear_uploads


@bot.message_handler(commands=["IMAGE"])
@command_handler()
def image_main(message: Message) -> None:
    """Обработчик команды IMAGE. Показывает доступные действия."""
    logger.info(f'{message.from_user.id}: /IMAGE')
    bot.send_message(
        message.from_user.id,
        "🤖Вот что я могу делать с изображениями:\n"
        "\n/format - конвертация jpg в png\n"
        "\n/noisy - добавление шума🔣\n"
        "\n/monochrome - черно-белая палитра🔳"
    )
    bot.set_state(message.from_user.id, UserState.waiting_action_image, message.chat.id)


@bot.message_handler(state=UserState.waiting_action_image)
@command_handler(state_required=UserState.waiting_action_image)
def image_select_action(message: Message) -> None:
    """Обработка выбора действия для изображения."""
    logger.info(f'{message.from_user.id}: Выбранное действие - {message.text}')
    command = message.text.lstrip('/')
    if command not in ["format", "noisy", "monochrome"]:
        bot.reply_to(message, "Неверная команда. Выберите из предложенного списка.")
        return

    bot.send_message(message.from_user.id, "🤖Пришлите изображение для обработки (не файл, или нажмите сжать).")
    bot.set_state(message.from_user.id, UserState.waiting_image, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["command"] = command


@bot.message_handler(content_types=['photo'], state=UserState.waiting_image)
@command_handler(state_required=UserState.waiting_image)
def image_process(message: Message) -> None:
    """Обработка изображения в зависимости от команды."""
    logger.info(f'{message.from_user.id}: Получено изображение.')

    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_name = file_info.file_path.split('/')[-1]
    user_path = os.path.join(uploads_path, str(message.from_user.id))
    os.makedirs(user_path, exist_ok=True)

    save_path = os.path.join(user_path, file_name)
    new_file_path = os.path.join(user_path, f"processed_{file_name}")

    try:
        downloaded_file = bot.download_file(file_info.file_path)
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            command = data.get("command")

        COMMANDS = {
            "monochrome": get_monochrome,
            "noisy": lambda src, dest: get_noise(src, dest, noise_level=0.1),
            "format": lambda src, _: format_replace(src),
        }

        action = COMMANDS.get(command)
        if action:
            result = action(save_path, new_file_path)
            if isinstance(result, str):
                new_file_path = result
            if result:
                with open(new_file_path, 'rb') as file:
                    bot.send_document(message.chat.id, file)
                logger.info(f'{message.from_user.id}: Изображение обработано и отправлено.')
                clear_uploads.main(message.from_user.id)
            else:
                error_handler.main(message, f"Ошибка обработки команды {command}")
        else:
            error_handler.main(message, "Неизвестная команда.")

    except Exception as e:
        logger.error(f"Ошибка при обработке изображения: {e}")
        error_handler.main(message, "Ошибка при обработке изображения.")
