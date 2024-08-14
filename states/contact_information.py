from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    """Класс состояний пользователя"""
    converting = State()
    waiting_target_format = State()
    waiting_format = State()
    waiting_file = State()
