from config_data.config import DEFAULT_COMMANDS
from loader import bot
from telebot.types import Message, ReplyKeyboardRemove


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    """
    Обработчик команды <help>.
    Выводит список команд.
    :param message: Полученное в чате сообщение
    :return:
    """
    text = ("При возникновении ошибки бот возвращается в начало диалога.\n"
            
            "\nФункционал бота:\n"
            "\nPDF:\n"
            "  - Конвертация в docx формат\n"
            "  - Конвертация в аудиокнигу\n"
            "\nИзображения:\n"
            "  - Конвертация в монохром\n"
            "  - Добавление шума\n"
            "  - Удаление фона\n"
            "\nКонвертация изображений из png в jpg и обратно\n"
            "\nГенерация штрих-кода\n"
            "\nПолучение кода HTML страницы\n"
            "\nПолучение информации об IP\n"
            
            "\nОбратная связь:\n"
            "Telegram: https://t.me/mr_dagestan\n"
            "Email: alexeyrodimkin@gmail.com")
    bot.reply_to(message, text, reply_markup=(ReplyKeyboardRemove()))
