from pdf2docx import Converter
import os
from PIL import Image, ImageOps
import random

uploads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))


def pdf_to_docx(pdf: str, docx: str) -> bool:
    """
    pdf2docx
    Функция конвертирования pdf -> docx
    :param pdf: str: путь к файлу
    :param docx: str: имя документа
    :return: bool
    """
    try:
        cv = Converter(pdf)  # Создаем конвертер
        cv.convert(docx, start=0, end=None)  # Конвертируем PDF в DOCX
        cv.close()  # Закрываем конвертер
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False


def delete_file(obj: str) -> bool:
    """
    Функция удаления
    :param obj: str: путь к файлу
    :return: bool
    """
    try:
        os.remove(obj)
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False


def convert_to_bw(file_path: str, new_file_path: str) -> bool:
    """
    PIL
    Функция конвертирования картинки в черно-белую
    :param file_path: str: путь к файлу
    :param new_file_path: str: путь к новому файлу
    :return: bool
    """
    try:
        img = Image.open(file_path)
        img = img.convert('L')
        img.save(new_file_path)
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False


def add_noise(file_path: str, noise_level=1):
    """
    Функция добавления шума к фото с использованием PIL
    :param file_path: str: путь к файлу
    :param noise_level: float: уровень шума (доля пикселей, к которым добавляется шум)
    :return: bool
    """
    try:
        # Открываем изображение и конвертируем его в формат RGB
        img = Image.open(file_path).convert('RGB')

        # Проходим по каждому пикселю изображения
        for x in range(img.width):
            for y in range(img.height):
                r, g, b = img.getpixel((x, y))
                # Добавляем шум к случайным пикселям с вероятностью noise_level
                if random.random() < noise_level:
                    # Добавляем случайные значения к каналам RGB и следим за границами 0-255
                    r = max(0, min(255, r + random.randint(-20, 20)))
                    g = max(0, min(255, g + random.randint(-20, 20)))
                    b = max(0, min(255, b + random.randint(-20, 20)))
                    img.putpixel((x, y), (r, g, b))

        # Сохраняем изображение с шумом
        new_name = os.path.join(uploads_path, "new_noisy." + file_path.split('.')[-1])
        img.save(new_name)
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

