from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    """Класс состояний пользователя"""

    # PDF states
    converting = State()
    waiting_target_format = State()
    waiting_format = State()
    waiting_file_pdf = State()

    # IMAGE states
    waiting_action_image = State()
    waiting_image = State()

    # barcode states
    waiting_numbers = State()

    # html
    waiting_link = State()


