from loader import bot
from telebot.types import Message
from handlers import error_handler
from utils.misc.algorithms import get_ip
from loguru import logger
from handlers.handler_decorator import command_handler
from states.states import UserState


@bot.message_handler(commands=["IP"])
@command_handler()
def ip_main(message: Message) -> None:
    """Обработчик команды IP"""
    logger.info(f'{message.from_user.id}: /IP')
    bot.send_message(message.from_user.id, "🤖Пришлите IP")
    bot.set_state(message.from_user.id, UserState.waiting_ip, message.chat.id)


@bot.message_handler(state=UserState.waiting_ip)
@command_handler(state_required=UserState.waiting_ip)
def get_ip_data(message: Message) -> None:
    """Обработчик ip"""
    logger.info(f'{message.from_user.id}: {message.text}.')
    data = get_ip(message.text)
    if data:
        result = (f"IP:                 {data['query']}\n"
                  f"City:             {data['city']}\n"
                  f"ISP:              {data['isp']}\n"
                  f"Country:     {data['country']}\n"
                  f"Region:       {data['region']}\n"
                  f"Timezone: {data['timezone']}")
        bot.send_message(message.from_user.id, result)
        bot.set_state(message.from_user.id, None, message.chat.id)
    else:
        error_handler.main(message, "Неверный IP-адрес")
