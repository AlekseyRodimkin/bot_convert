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
    bot.send_message(message.from_user.id, f'🤖Приветствую: {message.from_user.first_name}\n'
                                           '\nСписок моих команд: \n'
                                           '\n/PDF - 📃работа с PDF файлами\n'
                                           '\n/BARCODE - 📜генерация штрих-кода \n'
                                           '\n/IMAGE - 🖼редактирование изображений\n'
                                           '\n/HTML - 📝получить код страницы\n'
                                           '\n/IP - 📶получить информацию о IP\n',
                     reply_markup=ReplyKeyboardRemove())
