from pdf2docx import Converter
import os
from PIL import Image, ImageOps
import random
import barcode
from barcode.writer import ImageWriter
from rembg import remove
import cv2
import requests

uploads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))


def pdf_to_docx(pdf_path: str, docx_name: str) -> bool:
    """
    pdf2docx
    Функция конвертирования pdf -> docx
    :param pdf_path: str: путь к файлу
    :param docx_name: str: имя документа
    :return: bool
    """
    try:
        cv = Converter(pdf_path)
        cv.convert(docx_name, start=0, end=None)
        cv.close()
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False


def get_monochrome(file_path: str, new_file_path: str) -> bool:
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


def get_noise(file_path: str, new_file_path: str, noise_level=1):
    """
    Функция добавления шума к фото с использованием PIL
    :param file_path: str: путь к файлу
    :param new_file_path: str: путь к новому файлу
    :param noise_level: float: уровень шума (доля пикселей, к которым добавляется шум)
    :return: bool
    """
    try:
        img = Image.open(file_path).convert('RGB')
        for x in range(img.width):
            for y in range(img.height):
                r, g, b = img.getpixel((x, y))
                if random.random() < noise_level:
                    r = max(0, min(255, r + random.randint(-20, 20)))
                    g = max(0, min(255, g + random.randint(-20, 20)))
                    b = max(0, min(255, b + random.randint(-20, 20)))
                    img.putpixel((x, y), (r, g, b))

        img.save(new_file_path)
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False


def remove_background(file_path: str, new_file_path: str) -> bool:
    """
    Функция удаления фона из изображения
    :param file_path: str: путь к файлу
    :param new_file_path: str: путь к новому файлу
    :return: bool
    """
    try:
        input = cv2.imread(file_path)
        output = remove(input)
        cv2.imwrite(new_file_path, output)
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False


def get_html(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()

        if "text/html" not in response.headers.get("Content-Type", ""):
            print("Ответ не является HTML.")
            return ""

        response.encoding = response.apparent_encoding
        return response.text
    except requests.exceptions.Timeout:
        print("Истекло время ожидания запроса.")
    except requests.exceptions.ConnectionError:
        print("Ошибка соединения.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP ошибка: {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при запросе: {e}")
    return ""


def format_replace(file_path: str, ) -> str or bool:
    """
    Функция конвертирования png в jpg и обратно
    :param file_path: str: путь к файлу
    :return: bool
    """
    try:
        output_path = file_path.replace(".png", ".jpg") if file_path.endswith(".png") else file_path.replace(".jpg",
                                                                                                             ".png")
        image = Image.open(file_path)
        image.save(output_path)
        return output_path
    except Exception as e:
        print(f"Error occurred: {e}")
        return False


def get_barcode(numbers: str, new_file_path: str) -> bool:
    """
    Функция создания штрих-кода с использованием pyBarcode
    :param numbers: str: номера для штрих-кода
    :param new_file_path: str: путь к новому файлу
    :return: bool
    """
    try:
        barcode_number = numbers
        barcode_format = barcode.get_barcode_class('ean13')
        barcode_image = barcode_format(barcode_number, writer=ImageWriter())
        barcode_image.save(new_file_path)
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
