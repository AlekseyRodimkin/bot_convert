from loader import bot
from telebot.types import Message, ReplyKeyboardRemove
import os
from config_data.config import uploads_path
from loguru import logger


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    """
    Обработчик команды <start>.
    Выводит приветствие по имени пользователя.
    Выводит таблицу команд.
    Создает песональную папку в uploads
    Удаляет состояние
    :param message: Полученное в чате сообщение
    :return:
    """
    logger.info(f'{message.from_user.id}: /start')

    os.makedirs(f'{uploads_path}/{message.from_user.id}', exist_ok=True)
    logger.debug(f'mkdir: uploads/{message.from_user.id}')

    bot.delete_state(message.from_user.id)
    bot.send_message(message.from_user.id, f'🤖Приветствую: {message.from_user.first_name}\n'
                                           '\nСписок моих команд: \n'
                                           '\n/PDF - 📃работа с PDF файлами\n'
                                           '\n/BARCODE - ⏸генерация 12 значного штрих-кода \n'
                                           '\n/QR - 🔲генерация qr кода для ссылки или текста \n'
                                           '\n/IMAGE - 🖼редактирование изображений\n'
                                           '\n/HTML - 📝получить код страницы\n'
                                           '\n/IP - 📶получить информацию о IP\n',
                     reply_markup=ReplyKeyboardRemove())
