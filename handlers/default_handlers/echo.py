from telebot.types import Message
from loader import bot
from keyboards.reply.contact import start_buttons
from loguru import logger


# logger.add('logs/debug.log', format="{time} {level}    {message}", level="DEBUG")


@bot.message_handler(state=None)
def bot_echo(message: Message):
    """
    Обработчик сообщений без указанного состояния
    :param message: Полученное в чате сообщение
    :return:
    """
    if (message.text).lower() == "привет":
        bot.send_message(message.from_user.id, f"Привет, {message.from_user.username}")
        bot.send_message(message.from_user.id, "Выберите команду:", reply_markup=start_buttons())
    else:
        logger.debug(f"/echo -> {message.text}")
        bot.reply_to(message, "Я тебя не понимаю, напиши 'Привет' или /start")
