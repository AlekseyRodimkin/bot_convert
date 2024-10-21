from loader import bot
from states.states import UserState
from telebot.types import Message
from Exeptions.exeptions_classes import FileFormatError
import os
from handlers.custom_handlers.algorithms import get_monochrome, get_noise, remove_background, format_replace
from handlers.custom_handlers.errors import clearing_uploads, handle_error

uploads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))


# Функция для отправки сообщения с командами
def send_image_options(user_id: int):
    bot.send_message(user_id, "🤖Вот что я могу делать с изображениями:\n"
                              "\n/format - конвертация jpg в png и обратно🔄\n"
                              "\n/back - удаление фона с изображения🔵\n"
                              "\n/noisy - добавление шума🔣\n"
                              "\n/monochrome - конвертирование в черно-белую палитру🔳")


# Функция для отправки файла
def send_file(chat_id: int, file_path: str):
    with open(file_path, 'rb') as file:
        bot.send_document(chat_id, file)


# Функция для выполнения команды над изображением
def process_image_command(command, save_path, new_file_path, message):
    if command == "monochrome" and get_monochrome(save_path, new_file_path):
        send_file(message.chat.id, new_file_path)
    elif command == "noisy" and get_noise(save_path, new_file_path):
        send_file(message.chat.id, new_file_path)
    elif command == "back" and remove_background(save_path, new_file_path):
        send_file(message.chat.id, new_file_path)
    elif command == "format":
        result = format_replace(save_path)
        if result:
            result_format = result.split('.')[-1]
            user_format = "jpg" if result_format == 'png' else "png"
            bot.send_message(message.from_user.id, f"Исходный формат: {user_format}\n"
                                                   f"Новый формат: {result_format}")
            send_file(message.chat.id, result)
        else:
            handle_error(message, "Ошибка конвертации")
    else:
        handle_error(message, "Неверное действие")


# Обработчик команды конвертации IMAGE
@bot.message_handler(commands=["IMAGE"])
def image(message: Message) -> None:
    send_image_options(message.from_user.id)
    bot.set_state(message.from_user.id, UserState.waiting_action_image, message.chat.id)


# Обработчик выбора действия
@bot.message_handler(state=UserState.waiting_action_image)
def waiting_action_image(message: Message) -> None:
    if message.text == '/start':
        bot.delete_state(message.from_user.id)
        bot.send_message(message.from_user.id, "Вы вышли из режима работы с изображениями")
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["command"] = message.text[1:]

    bot.send_message(message.from_user.id, f"🤖Пришлите изображение")
    bot.set_state(message.from_user.id, UserState.waiting_image, message.chat.id)


# Обработчик получения изображения
@bot.message_handler(content_types=['photo'], state=UserState.waiting_image)
def waiting_image(message: Message) -> None:
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_name = file_info.file_path.split('/')[1]
    save_path = os.path.join(uploads_path, file_name)

    try:
        downloaded_file = bot.download_file(file_info.file_path)
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "🤖Конвертирую...")

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            command = data.get("command")
            new_file_path = os.path.join(uploads_path, f"{command}_{file_name}")
            process_image_command(command, save_path, new_file_path, message)

    except FileFormatError:
        handle_error(message, "Некорректное расширение")
    finally:
        bot.set_state(message.from_user.id, None, message.chat.id)
        clearing_uploads()
