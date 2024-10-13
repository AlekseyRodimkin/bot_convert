from loader import bot
from states.states import UserState
from telebot.types import Message, ReplyKeyboardRemove
from Exeptions.exeptions_classes import FileFormatError
import os
from handlers.custom_handlers.algorithms import convert_to_bw, delete_file, add_noise, remove_background

uploads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))


@bot.message_handler(commands=["IMAGE"])
def image(message: Message) -> None:
    """
    Обработчик команды конвертации IMAGE.
    Переводит в состояние "Ожидание целевого действия".
    :param message: Полученное в чате сообщение (команда)
    :return
    """
    bot.send_message(message.from_user.id, "🤖Вот что я могу делать с изображениями: \n"
                                           "\n/dark - конвертирование в черно-белую палитру🔳\n"
                                           "/noisy - добавление шума🔣\n"
                                           "/background - удаление фона с изображения🔵")
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
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["command"] = message.text[1:]
    bot.send_message(message.from_user.id, f"🤖Пришлите изображение")
    bot.set_state(message.from_user.id, UserState.waiting_image, message.chat.id)


def handle_conversion_error(message, error_code, save_path=None):
    """Обработчик ошибок с завершением состояния и удалением файла."""
    if save_path:
        delete_file(save_path)
    bot.set_state(message.from_user.id, None, message.chat.id)
    bot.send_message(message.chat.id,
                     f"🤖‼️Возникла ошибка (код ошибки {error_code})\nПожалуйста, сообщите в поддержку: \n👨‍💻 /help")


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

        if not file_name.lower().endswith(('jpg', 'png')):
            raise FileFormatError()

        bot.reply_to(message, "🤖Конвертирую...")

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            command = data.get("command")
            new_file_prefix = "monochrome_" if command == "dark" else "new_"
            path_to_new_file = os.path.join(uploads_path, new_file_prefix + file_name)

            if command == "dark" and convert_to_bw(save_path, path_to_new_file):
                bot.send_document(message.chat.id, open(path_to_new_file, 'rb'))
            elif command == "noisy" and add_noise(save_path):
                bot.send_document(message.chat.id, open(path_to_new_file, 'rb'))
            elif command == "background" and remove_background(save_path, path_to_new_file):
                bot.send_document(message.chat.id, open(path_to_new_file, 'rb'))
            else:
                handle_conversion_error(message, "img.02", save_path)
                return

            delete_file(save_path)
            delete_file(path_to_new_file)
            bot.set_state(message.from_user.id, None, message.chat.id)

    except FileFormatError:
        """Ошибка формата файла"""
        handle_conversion_error(message, "Некорректное расширение", save_path)

    except FileNotFoundError as e:
        """Ошибка пути"""
        print(f"Error occurred: {e}")
        handle_conversion_error(message, "img.01", save_path)

    finally:
        bot.set_state(message.from_user.id, None, message.chat.id)