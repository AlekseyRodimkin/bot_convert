from loader import bot
from states.states import UserState
from telebot.types import Message, ReplyKeyboardRemove
from Exeptions.exeptions_classes import FileFormatError
import os
from handlers.custom_handlers.algorithms import pdf_to_docx, delete_file
from handlers.custom_handlers.algorithms import convert_to_bw

uploads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))


@bot.message_handler(commands=["IMAGE"])
def image(message: Message) -> None:
    """
    Обработчик команды конвертации IMAGE.
    Переводит в состояние "Ожидание целевого действия".
    :param message: Полученное в чате сообщение (команда)
    :return
    """
    bot.send_message(message.from_user.id, "Вот что я могу делать с изображениями: \n"
                                           "\n/dark - Конвертирование в черно-белую палитру")
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
    bot.send_message(message.from_user.id, f"Пришлите изображение")
    bot.set_state(message.from_user.id, UserState.waiting_image, message.chat.id)


@bot.message_handler(content_types=['photo'], state=UserState.waiting_image)
def waiting_image(message: Message) -> None:
    """
    Обработчик целевого действия
    Переводит в состояние ".................................................."
    Вызывает функцию ..................................
    :param message: Полученное в чате сообщение
    :return:
    """
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_name = file_info.file_path.split('/')[1]
    file_path = file_info.file_path
    downloaded_file = bot.download_file(file_path)
    save_path = os.path.join(uploads_path, file_name)

    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    try:
        if not file_name.endswith('jpg') and not file_name.endswith('png'):
            raise FileFormatError()
        bot.reply_to(message, "Конвертирую...")
        path_to_new_file = os.path.join(uploads_path, "bw_" + file_name)

        if convert_to_bw(save_path, path_to_new_file):
            bot.send_document(message.chat.id, open(path_to_new_file, 'rb'))
            delete_file(save_path)
            delete_file(path_to_new_file)
            bot.set_state(message.from_user.id, None, message.chat.id)
            return
        else:
            bot.send_message(message.chat.id,
                             "Ошибка конвертирования, попробуйте еще раз или сообщите о проблеме по команде /help")
            bot.set_state(message.from_user.id, None, message.chat.id)
            delete_file(save_path)
            return

    except FileFormatError:
        """Ошибка формата файла"""
        # delete_file(save_path)
        bot.set_state(message.from_user.id, None, message.chat.id)
        bot.send_message(message.from_user.id,
                         f"Не корректное расширение исходного файла, нажмите /start чтобы получить список команд")
        return
