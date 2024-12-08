import os
import random
from io import BytesIO
from config_data.config import uploads_path
from pdf2docx import Converter
from PIL import Image, ImageFont, ImageDraw
from loguru import logger
from gtts import gTTS
import qrcode
import pdfplumber as pp
import requests
from rembg import remove
import cv2
import numpy as np
import barcode
from barcode.writer import ImageWriter
from urllib.parse import urlparse


def safe_execute(func, *args, **kwargs):
    """Универсальный обработчик ошибок."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Ошибка в {func.__name__}: {e}")
        return None


def is_valid_url(url: str):
    logger.debug("is_valid_url()")
    return safe_execute(lambda: _is_valid_url(url))


def _is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def text_to_audio(text: str, lang: str = 'ru') -> BytesIO or None:
    logger.debug("text_to_audio()")
    return safe_execute(lambda: _text_to_audio(text, lang))


def _text_to_audio(text: str, lang: str) -> BytesIO:
    tts = gTTS(text=text, lang=lang)
    audio_stream = BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)
    return audio_stream


def pdf_to_audio(file_path: str, new_file_path: str):
    logger.debug("pdf_to_audio()")
    return safe_execute(lambda: _pdf_to_audio(file_path, new_file_path))


def _pdf_to_audio(file_path: str, new_file_path: str):
    pdf_text = ''
    with pp.open(file_path) as pdf:
        for page in pdf.pages:
            pdf_text += page.extract_text()
    tts = gTTS(text=pdf_text, lang='ru')
    tts.save(new_file_path)
    logger.debug(f'pdf_to_book(file_path) : saved')
    return True


def text_to_image(text: str) -> BytesIO or None:
    logger.debug("text_to_image()")
    return safe_execute(lambda: _text_to_image(text))


def _text_to_image(text: str) -> BytesIO:
    font = ImageFont.load_default()
    img = Image.new('RGB', (500, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), text, font=font, fill=(0, 0, 0))

    image_stream = BytesIO()
    img.save(image_stream, format='PNG')
    image_stream.seek(0)
    return image_stream


def pdf_to_docx(file_path: str, docx_name: str) -> bool:
    logger.debug("pdf_to_docx()")
    return safe_execute(lambda: _pdf_to_docx(file_path, docx_name))


def _pdf_to_docx(file_path: str, docx_name: str) -> bool:
    cv = Converter(file_path)
    cv.convert(docx_name, start=0, end=None)
    cv.close()
    return True


def remove_background(file_path: str, new_file_path: str) -> bool:
    logger.debug("remove_background()")
    return safe_execute(lambda: _remove_background(file_path, new_file_path))


def _remove_background(file_path: str, new_file_path: str) -> bool:
    input_image = cv2.imread(file_path)
    output = remove(input_image)
    cv2.imwrite(new_file_path, output)
    return True


def get_noise(file_path: str, new_file_path: str, noise_level=0.1) -> bool:
    logger.debug("get_noise()")
    return safe_execute(lambda: _get_noise(file_path, new_file_path, noise_level))


def _get_noise(file_path: str, new_file_path: str, noise_level: float) -> bool:
    img = Image.open(file_path).convert('RGB')
    img_data = np.array(img)

    noise = np.random.randint(-20, 20, img_data.shape, dtype='int16')
    mask = np.random.random(img_data.shape[:2]) < noise_level

    img_data = np.clip(img_data + noise * mask[:, :, None], 0, 255).astype('uint8')
    Image.fromarray(img_data).save(new_file_path)
    return True


def get_html(url: str) -> str or None:
    logger.debug("get_html()")
    return safe_execute(lambda: _get_html(url))


def _get_html(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
    response.raise_for_status()

    if "text/html" not in response.headers.get("Content-Type", ""):
        raise ValueError("Ответ не является HTML")

    response.encoding = response.apparent_encoding
    return response.text


def get_qr(data: str) -> BytesIO or None:
    logger.debug("get_qr()")
    return safe_execute(lambda: _get_qr(data))


def _get_qr(data: str) -> BytesIO:
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    qr_stream = BytesIO()
    img.save(qr_stream, format='PNG')
    qr_stream.seek(0)
    return qr_stream


def get_barcode(data: str, new_file_path: str):
    logger.debug("get_barcode()")
    return safe_execute(lambda: _get_barcode(data, new_file_path))


def _get_barcode(data: str, new_file_path: str) -> bool:
    barcode_number = data
    barcode_format = barcode.get_barcode_class('ean13')
    barcode_image = barcode_format(barcode_number, writer=ImageWriter())
    barcode_image.save(new_file_path)
    return True


def get_monochrome(file_path, new_file_path):
    logger.debug("get_monochrome()")
    return safe_execute(lambda: _get_monochrome(file_path, new_file_path))


def _get_monochrome(file_path: str, new_file_path: str) -> bool:
    img = Image.open(file_path)
    img = img.convert('L')
    img.save(new_file_path)
    return True


def get_ip(ip: str):
    logger.debug("get_ip()")
    return safe_execute(lambda: _get_ip(ip))


def _get_ip(ip: str) -> None or dict:
    logger.debug(f'get_ip_info({ip})')
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "fail":
        logger.error(f"get_ip_info({ip}): Error: {data['message']}")
        return
    return data


def format_replace(file_path: str):
    logger.debug("format_replace()")
    return safe_execute(lambda: _format_replace(file_path))


def _format_replace(file_path: str, ) -> str:
    output_path = file_path.replace(".jpg", ".png")
    image = Image.open(file_path)
    image.save(output_path)
    logger.debug(f'format_replace(file_path) : saved')
    return output_path
