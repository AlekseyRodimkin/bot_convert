from loader import bot
from states.states import UserState
from telebot.types import Message
from handlers.custom_handlers.algorithms import get_ip_info
from handlers.custom_handlers.errors import handle_error


@bot.message_handler(commands=["IP"])
def ip_start(message: Message) -> None:
    """
    Обработчик команды получения информации о IP.
    Переводит в состояние "Ожидание IP".
    :param message: Полученное в чате сообщение (команда)
    :return
    """
    bot.send_message(message.from_user.id, "🤖Пришлите IP")
    bot.set_state(message.from_user.id, UserState.waiting_ip, message.chat.id)


@bot.message_handler(state=UserState.waiting_ip)
def waiting_ip(message: Message) -> None:
    """
    Обработчик ip
    :param message: Полученное в чате сообщение
    :return:
    """
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
        handle_error(message, "Неверный IP-адрес")
