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
                                           '\n/PDF - для конвертации PDF документ в формат DOCX (word) \n'
                                           '/IMAGE - для работы с изображением\n',
                     reply_markup=ReplyKeyboardRemove())
