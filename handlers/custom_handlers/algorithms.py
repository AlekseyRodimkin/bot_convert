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
    Функция конвертирования в черно-белую
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

    # def change_size():
    #     """Изменение размера картинки"""
        # img_resized = img.resize((640, 480))
        # img_resized.save('resized_example.jpg')
        # pass

    # def add_noise(image, noise_level=0.05):
    #     """Добавление шума"""
    #     width, height = image.size
    #     for x in range(width):
    #         for y in range(height):
    #             r, g, b = image.getpixel((x, y))
    #             if random.random() < noise_level:
    #                 image.putpixel((x, y), (r + random.randint(-20, 20), g + random.randint(-20, 20), b + random.randint(-20, 20)))
    #     return image
    #
    #
    # # добавление шума к измененной картинке
    # img_noisy = add_noise(img_resized)
    # img_noisy.save('noisy_example.jpg')
    #
    #
    # # добавление фона
    # def add_background(image, background_color=(255, 255, 255)):
    #     width, height = image.size
    #     new_image = Image.new('RGB', (width, height + 100), background_color)
    #     new_image.paste(image, (0, 100))
    #     return new_image
    #
    #
    # # добавление фона к измененной картинке
    # img_background = add_background(img_noisy)
    # img_background.save('background_example.jpg')
