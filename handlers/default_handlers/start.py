from loader import bot
from telebot.types import Message, ReplyKeyboardRemove


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    """
    Обработчик команды <start>.
    Выводит приветствие по имени пользователя.
    Выводит таблицу команд.
    :param message: Полученное в чате сообщение
    :return:
    """
    bot.delete_state(message.from_user.id)
    bot.send_message(message.from_user.id, f'Приветствую {message.from_user.first_name}\n'
                                           '\nСписок моих команд: \n'
                                           '\n/PDF - конвертация PDF документа в формат DOCX (word) \n'
                                           '/BAR - генерация штрих-кода \n'
                                           '/IMAGE - редактирование изображений\n',
                     reply_markup=ReplyKeyboardRemove())
