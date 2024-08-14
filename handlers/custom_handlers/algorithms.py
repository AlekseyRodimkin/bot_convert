from loguru import logger
from pdf2docx import Converter
import os


def pdf_to_docx(pdf: str, docx: str) -> None:
    """
    Функция конвертирования pdf -> docx
    :param pdf: str: путь к файлу
    :param docx: str: имя документа
    :return: None
    """
    logger.debug("func -> pdf_to_docx")
    cv = Converter(pdf)  # Создаем конвертер
    cv.convert(docx, start=0, end=None)  # Конвертируем PDF в DOCX
    cv.close()  # Закрываем конвертер
    logger.debug(f"File converted to {docx}")


def delete_docs(obj: str) -> None:
    """
    Функция удаления
    :param obj: str: путь к файлу
    :return: None
    """
    os.remove(obj)
