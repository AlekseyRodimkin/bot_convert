from loader import bot
from telebot.types import Message
from loguru import logger


@bot.message_handler(state=None)
def bot_echo(message: Message):
    """
    Обработчик сообщений без указанного состояния
    :param message: Полученное в чате сообщение
    :return:
    """
    logger.info(f'{message.from_user.id}: /echo: {message.text}')

    bot.delete_state(message.from_user.id)
    bot.reply_to(message, "Я тебя не понимаю\n"
                          "Напиши /start для перезапуска бота или /help")
