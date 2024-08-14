from loader import bot
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
import handlers
from loguru import logger

logger.add('logs/debug.log', format="{time} {level}    {message}", level="INFO")
logger.add('logs/debug.log', format="{time} {level}    {message}", level="ERROR")
logger.add('logs/debug.log', format="{time} {level}    {message}", level="DEBUG")

if __name__ == '__main__':
    with open("logs/debug.log", 'w') as info_log:
        """Очистка логов"""

    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
