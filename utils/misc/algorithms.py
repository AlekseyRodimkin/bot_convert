from config_data.config import uploads_path
from pdf2docx import Converter
import os
from PIL import Image, ImageOps
import random
import barcode
from barcode.writer import ImageWriter
from rembg import remove
import cv2
import requests
import pdfplumber as pp
from gtts import gTTS
import qrcode
from io import BytesIO
from loguru import logger


def pdf_to_docx(file_path: str, docx_name: str) -> bool or None:
    """
    pdf2docx
    Функция конвертирования pdf -> docx
    :param file_path: str: путь к файлу
    :param docx_name: str: имя документа
    :return: bool
    """
    try:
        logger.debug(f'pdf_to_docx(file_path)')
        cv = Converter(file_path)
        cv.convert(docx_name, start=0, end=None)
        cv.close()
        logger.debug(f'pdf_to_docx(docx_name) : saved')
        return True
    except Exception as e:
        logger.error(f"pdf_to_docx(file_path): {e}")
        return


def pdf_to_book(file_path: str, new_file_path: str):
    """
    pdfplumber
    Функция создания книги из pdf
    :param file_path: str: путь к файлу
    :param new_file_path: str: путь к новой книге
    :return: bool
    """
    try:
        logger.debug(f'pdf_to_book(file_path)')
        pdf_text = ''
        with pp.open(file_path) as pdf:
            for page in pdf.pages:
                pdf_text += page.extract_text()
        tts = gTTS(text=pdf_text, lang='ru')
        tts.save(new_file_path)
        logger.debug(f'pdf_to_book(file_path) : saved')
        return True
    except Exception as e:
        logger.error(f"pdf_to_book(file_path): {e}")
        return


def get_monochrome(file_path: str, new_file_path: str) -> bool or None:
    """
    PIL
    Функция конвертирования картинки в черно-белую
    :param file_path: str: путь к файлу
    :param new_file_path: str: путь к новому файлу
    :return: bool
    """
    try:
        logger.debug(f'get_monochrome(file_path)')
        img = Image.open(file_path)
        img = img.convert('L')
        img.save(new_file_path)
        logger.debug(f'get_monochrome(url) : saved')
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return


def get_noise(file_path: str, new_file_path: str, noise_level=1) -> bool or None:
    """
    Функция добавления шума к фото с использованием PIL
    :param file_path: str: путь к файлу
    :param new_file_path: str: путь к новому файлу
    :param noise_level: float: уровень шума (доля пикселей, к которым добавляется шум)
    :return: bool
    """
    try:
        logger.debug(f'get_noise(file_path)')
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
        logger.debug(f'get_noise(url) : saved')
        return True
    except Exception as e:
        logger.error(f"get_noise(file_path): {e}")
        return


def remove_background(file_path: str, new_file_path: str) -> bool or None:
    """
    Функция удаления фона из изображения
    :param file_path: str: путь к файлу
    :param new_file_path: str: путь к новому файлу
    :return: bool
    """
    try:
        logger.debug(f'remove_background(file_path)')
        input = cv2.imread(file_path)
        output = remove(input)
        cv2.imwrite(new_file_path, output)
        logger.debug(f'remove_background(url) : saved')
        return True
    except Exception as e:
        logger.error(f"remove_background(file_path): {e}")
        return


def get_html(url):
    try:
        logger.debug(f'get_html({url})')

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()

        if "text/html" not in response.headers.get("Content-Type", ""):
            logger.debug(f"get_html({url}): Ответ не является HTML.")
            return ""

        response.encoding = response.apparent_encoding
        return response.text
    except requests.exceptions.Timeout:
        logger.error(f"get_html({url}): Истекло время ожидания запроса")
    except requests.exceptions.ConnectionError:
        logger.error(f"get_html({url}): Ошибка соединения")
    except requests.exceptions.HTTPError as e:
        logger.error(f"get_html({url}): HTTP ошибка: {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"get_html({url}): Произошла ошибка при запросе: {e}")
    return ""


def format_replace(file_path: str, ) -> str or None:
    """
    Функция конвертирования png в jpg и обратно
    :param file_path: str: путь к файлу
    :return: bool
    """
    try:
        logger.debug(f'format_replace(file_path)')

        output_path = file_path.replace(".jpg", ".png")
        image = Image.open(file_path)
        image.save(output_path)
        logger.debug(f'format_replace(file_path) : saved')
        return output_path
    except Exception as e:
        logger.error(f"format_replace(file_path): {e}")
        return


def get_barcode(numbers: str, new_file_path: str) -> bool or None:
    """
    Функция создания штрих-кода с использованием pyBarcode
    :param numbers: str: номера для штрих-кода
    :param new_file_path: str: путь к новому файлу
    :return: bool
    """
    try:
        logger.debug(f'get_barcode({numbers})')
        barcode_number = numbers
        barcode_format = barcode.get_barcode_class('ean13')
        barcode_image = barcode_format(barcode_number, writer=ImageWriter())
        barcode_image.save(new_file_path)
        logger.debug(f'get_barcode(new_file_path) : saved')
        return True
    except Exception as e:
        logger.error(f"get_barcode({numbers}): {e}")
        return


def get_ip_info(ip: str) -> None or dict:
    """
    Функция получения информации о IP адресе
    :param ip: str: IP адрес
    :return: dict or None
    """
    try:
        logger.debug(f'get_ip_info({ip})')
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        data = response.json()
        if data["status"] == "fail":
            logger.error(f"get_ip_info({ip}): Error: {data['message']}")
            return
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"get_ip_info({ip}): {e}")
        return


def get_qr(data: str) -> BytesIO or bool:
    """
    Функция для генерации qr кода
    :param data: str: сообщение пользователя
    :return: BytesIO or bool
    """
    try:
        logger.debug(f'get_qr({data})')

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        logger.debug(f'get_qr(data) : saved')

        return img_byte_arr
    except Exception as e:
        logger.error(f"get_qr(data): {e}")
        return
