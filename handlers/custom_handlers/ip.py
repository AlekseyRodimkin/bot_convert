from loader import bot
from states.states import UserState
from telebot.types import Message
from utils.misc import error_handler
from utils.misc.algorithms import get_ip_info
from loguru import logger



@bot.message_handler(commands=["IP"])
def main(message: Message) -> None:
    """
    Обработчик команды получения информации о IP.
    Переводит в состояние "Ожидание IP".
    :param message: Полученное в чате сообщение (команда)
    """
    logger.info(f'{message.from_user.id}: /IP')
    bot.send_message(message.from_user.id, "🤖Пришлите IP")
    bot.set_state(message.from_user.id, UserState.waiting_ip, message.chat.id)


@bot.message_handler(state=UserState.waiting_ip)
def waiting_ip(message: Message) -> None:
    """
    Обработчик ip
    :param message: Полученное в чате сообщение
    """
    logger.info(f'{message.from_user.id}: waiting_ip({message.text})')
    data = get_ip_info(message.text)
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
