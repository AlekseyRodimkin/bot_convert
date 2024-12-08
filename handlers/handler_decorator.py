from loader import bot
from telebot.types import Message, ReplyKeyboardRemove
from handlers import error_handler
from loguru import logger
from utils.misc import clear_uploads


def command_handler(state_required=None):
    """Декоратор для обработки команд с проверкой состояния."""

    def decorator(func):
        def wrapper(message: Message):
            try:
                # if state_required and bot.get_state(message.from_user.id) != str(state_required):
                #     bot.reply_to(message, "🤖 Ожидал другую команду.\n")
                #     return
                if message.text == '/start':
                    clear_uploads.main(message.from_user.id)
                    bot.set_state(message.from_user.id, None, message.chat.id)
                    bot.send_message(message.chat.id,
                                     f"🤖 Завершил работу, теперь используйте /start", reply_markup=ReplyKeyboardRemove())
                    logger.info(f'{message.from_user.id}: state=None')
                    return
                result = func(message)
                return result
            except Exception as e:
                logger.error(f"Ошибка в {func.__name__}: {e}")
                error_handler.main(message, "Произошла внутренняя ошибка")

        return wrapper

    return decorator
