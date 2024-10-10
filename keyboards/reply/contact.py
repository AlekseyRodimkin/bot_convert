from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def pdf_to_target() -> ReplyKeyboardMarkup:
    """
    Кнопки целевых форматов PDF
    :return keyboard
    """
    keyboard = ReplyKeyboardMarkup()
    keyboard.add((KeyboardButton("/DOCX")))
    return keyboard


def yes_or_no_button() -> ReplyKeyboardMarkup:
    """
    Кнопки <Да> и <Нет>
    :return: keyboard
    """
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton("Да"))
    keyboard.add(KeyboardButton("Нет"))
    return keyboard

