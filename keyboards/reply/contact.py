from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from loguru import logger

logger.add('logs/debug.log', format="{time} {level}    {message}", level="DEBUG")


def start_buttons() -> ReplyKeyboardMarkup:
    """
    Кнопки всех начальных форматов
    :return keyboard
    """
    keyboard = ReplyKeyboardMarkup()
    keyboard.add((KeyboardButton("/PDF")))
    keyboard.add((KeyboardButton("/JPG")))
    keyboard.add((KeyboardButton("/HTML")))
    keyboard.add((KeyboardButton("/DOC")))
    keyboard.add((KeyboardButton("/TEXT")))
    keyboard.add((KeyboardButton("/WORD")))
    keyboard.add((KeyboardButton("/Изображение_в...")))
    # keyboard.add((KeyboardButton("/PDF-DOCX")))
    # keyboard.add((KeyboardButton("/PDF-DOC")))
    # keyboard.add((KeyboardButton("/PDF-WORD")))
    # keyboard.add((KeyboardButton("/PDF-Изображение")))
    # keyboard.add((KeyboardButton("/PDF-XPS")))
    # keyboard.add((KeyboardButton("/PDF-JPG")))
    # keyboard.add((KeyboardButton("/PDF-PNG")))
    # keyboard.add((KeyboardButton("/JPG-WORD")))
    # keyboard.add((KeyboardButton("/HTML-Изображение")))
    # keyboard.add((KeyboardButton("/DOC-JPG")))
    # keyboard.add((KeyboardButton("/TEXT-PNG")))
    # keyboard.add((KeyboardButton("/WORD-JPG")))
    # keyboard.add((KeyboardButton("/Изображение-WORD")))
    # keyboard.add((KeyboardButton("/Изображение-TEXT")))
    # keyboard.add((KeyboardButton("/Изображение-HTML")))
    logger.debug('function -> start_buttons()')
    return keyboard


def pdf_to_target() -> ReplyKeyboardMarkup:
    """
    Кнопки целевых форматов PDF
    :return keyboard
    """
    keyboard = ReplyKeyboardMarkup()
    keyboard.add((KeyboardButton("/DOCX")))
    keyboard.add((KeyboardButton("/DOC")))
    keyboard.add((KeyboardButton("/WORD")))
    keyboard.add((KeyboardButton("/Изображение")))
    keyboard.add((KeyboardButton("/PNG")))
    keyboard.add((KeyboardButton("/JPG")))
    keyboard.add((KeyboardButton("/XPS")))
    logger.debug('function -> pdf_to()')
    return keyboard


def yes_or_no_button() -> ReplyKeyboardMarkup:
    """
    Кнопки <Да> и <Нет>
    :return: keyboard
    """
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton("Да"))
    keyboard.add(KeyboardButton("Нет"))
    logger.debug('function -> yes_or_no_button()')
    return keyboard

