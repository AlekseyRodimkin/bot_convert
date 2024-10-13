from loader import bot
from states.states import UserState
from telebot.types import Message
from Exeptions.exeptions_classes import FileFormatError
import os
from handlers.custom_handlers.algorithms import get_monochrome, get_noise, remove_background, \
    format_replace
from handlers.custom_handlers.errors import clearing_uploads, handle_error

uploads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))


@bot.message_handler(commands=["IMAGE"])
def image(message: Message) -> None:
    """
    Обработчик команды конвертации IMAGE.
    Переводит в состояние "Ожидание целевого действия".
    :param message: Полученное в чате сообщение (команда)
    :return
    """
    bot.send_message(message.from_user.id, "🤖Вот что я могу делать с изображениями:\n"
                                           "\n/format - конвертация jpg в png и обратно🔄\n"
                                           "\n/back - удаление фона с изображения🔵\n"
                                           "\n/noisy - добавление шума🔣\n"
                                           "\n/monochrome - конвертирование в черно-белую палитру🔳")
    bot.set_state(message.from_user.id, UserState.waiting_action_image, message.chat.id)


@bot.message_handler(state=UserState.waiting_action_image)
def waiting_action_image(message: Message) -> None:
    """
    Обработчик целевого действия
    Переводит в состояние ".................................................."
    Вызывает функцию ..................................
    :param message: Полученное в чате сообщение
    :return:
    """
    if message.text == '/start':
        bot.delete_state(message.from_user.id)
        bot.send_message(message.from_user.id, "Вы вышли из режима работы с изображениями")
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["command"] = message.text[1:]
    bot.send_message(message.from_user.id, f"🤖Пришлите изображение")
    bot.set_state(message.from_user.id, UserState.waiting_image, message.chat.id)


@bot.message_handler(content_types=['photo'], state=UserState.waiting_image)
def waiting_image(message: Message) -> None:
    """
    Обработчик получения изображения, конвертирует в ЧБ или добавляет шум
    :param message: Полученное в чате сообщение
    :return:
    """
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_name = file_info.file_path.split('/')[1]
    file_path = file_info.file_path
    save_path = os.path.join(uploads_path, file_name)

    try:
        downloaded_file = bot.download_file(file_path)
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "🤖Конвертирую...")

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            command = data.get("command")
            new_file_path = os.path.join(uploads_path, f"{command}_{file_name}")

            if command == "monochrome" and get_monochrome(save_path, new_file_path):
                bot.send_document(message.chat.id, open(new_file_path, 'rb'))
            elif command == "noisy" and get_noise(save_path, new_file_path):
                bot.send_document(message.chat.id, open(new_file_path, 'rb'))
            elif command == "back" and remove_background(save_path, new_file_path):
                bot.send_document(message.chat.id, open(new_file_path, 'rb'))
            elif command == "format":
                result = format_replace(save_path)
                if result:
                    result_format = result.split('.')[-1]
                    user_format = "jpg" if result_format == 'png' else "png"
                    bot.send_message(message.from_user.id, f"Исходный формат: {user_format}\n"
                                                           f"Новый формат: {result_format}")
                    bot.send_document(message.chat.id, open(result, 'rb'))
                else:
                    handle_error(message, "Ошибка конвертации")
            else:
                handle_error(message, "Неверное действие")
                return

    except FileFormatError:
        """Ошибка формата файла"""
        handle_error(message, "Некорректное расширение")

    finally:
        bot.set_state(message.from_user.id, None, message.chat.id)
        clearing_uploads()
