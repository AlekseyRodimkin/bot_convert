from loader import bot
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
import handlers
from loguru import logger

logger.add('logs/error.log', format="{time} {level} {message}", level="ERROR", rotation="10 MB", retention=5)
logger.add('logs/info.log', format="{time} {level} {message}", level="INFO", rotation="10 MB", retention=5)
logger.add('logs/debug.log', format="{time} {level} {message}", level="DEBUG", rotation="10 MB", retention=5)

if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
