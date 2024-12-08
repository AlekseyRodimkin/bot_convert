import yt_dlp
import sys
import subprocess
import requests
import os
from dotenv import load_dotenv
import json
from loguru import logger
import threading
from Exeptions.exeptions_classes import DiskGetLinkError, PublishingFileError, FileDownloadError
from config_data.config import uploads_path, disk_app_folder_name
from handlers import error_handler
from concurrent.futures import ThreadPoolExecutor

load_dotenv()
YA_TOKEN = os.getenv("YANDEX_DISK_TOKEN")
COOKIES_FILE = "./cookies.txt"


def get_video_name_from_uploads(id: str, format: str) -> str:
    """Возвращает имя видеофайла из директории загрузок пользователя."""
    logger.debug("youtube.get_video_name_from_uploads()")

    uploads_user_dir = os.path.join(uploads_path, id)
    for root, dirs, files in os.walk(uploads_user_dir):
        for file in files:
            if file.endswith(format):
                logger.debug(f"youtube.get_video_name_from_uploads() -> {file}")
                return file
        raise FileNotFoundError


def download_video(url, output_dir, cookies_file):
    """Загружает видео с YouTube и сохраняет его в указанную директорию."""
    logger.debug("youtube.download_video()")

    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")
    command = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "--merge-output-format", "mp4",
        "-o", output_template,
        "--write-info-json",
        "--cookies", cookies_file,
        url
    ]
    subprocess.run(command, check=True)
    return True


def upload_file_to_disk_folder(dir_path, file_name, disk_folder_path, ya_token):
    """
    Загружает файл на Яндекс.Диск в указанную директорию.

    :param dir_path: Путь к локальной директории
    :param file_name: Имя файла
    :param disk_folder_path: Путь на Яндекс.Диске
    :param ya_token: OAuth-токен для доступа к Яндекс.Диску
    :raises: FileDownloadError, DiskGetLinkError
    :return: True, если файл успешно загружен
    """
    logger.debug("youtube.upload_file_to_disk_folder()")
    url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {"Authorization": f"OAuth {ya_token}"}
    params = {"path": f"{disk_folder_path}/{file_name}", "overwrite": "true"}

    try:
        logger.debug("Выполняю запрос на диск для получения ссылки")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Выбросить исключение, если код не 2xx

        upload_url = response.json().get("href")
        if not upload_url:
            logger.error("Не удалось получить ссылку для загрузки")
            raise DiskGetLinkError("Не удалось получить ссылку для загрузки")
    except requests.RequestException as e:
        logger.error(f"Ошибка при получении ссылки: {e}")
        raise DiskGetLinkError(f"Ошибка при получении ссылки: {e}")

    path = os.path.join(dir_path, file_name)
    logger.debug(f"Путь к файлу: {path}")

    if not os.path.isfile(path):
        logger.error(f"Файл не найден: {path}")
        raise FileNotFoundError(f"Файл не найден: {path}")

    def upload_file():
        """Выполняет загрузку файла в отдельном потоке."""
        with open(path, "rb") as f:
            try:
                logger.debug("Начинаю загрузку файла на Яндекс.Диск")
                upload_response = requests.put(upload_url, files={"file": f})
                upload_response.raise_for_status()  # Проверить успешность запроса
                return upload_response.status_code
            except requests.RequestException as e:
                logger.error(f"Ошибка при загрузке файла: {e}")
                raise FileDownloadError(f"Ошибка при загрузке файла: {e}")

    # Выполняем загрузку в отдельном потоке
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(upload_file)
        try:
            status_code = future.result()  # Ждём завершения потока
            if status_code == 201:
                logger.debug("Файл успешно загружен")
                return True
            else:
                logger.error(f"Ошибка загрузки: статус {status_code}")
                raise FileDownloadError(f"Ошибка загрузки: статус {status_code}")
        except FileDownloadError as e:
            logger.error(f"Ошибка в процессе загрузки: {e}")
            raise


def get_file_shareable_link(file_path):
    """Публикует файл на Яндекс.Диске и возвращает публичную ссылку."""
    logger.debug("youtube.get_file_shareable_link()")

    url_publish = "https://cloud-api.yandex.net/v1/disk/resources/publish"
    headers = {"Authorization": f"OAuth {YA_TOKEN}"}
    params = {"path": file_path}

    response = requests.put(url_publish, headers=headers, params=params)
    if response.status_code == 200:
        url_meta = "https://cloud-api.yandex.net/v1/disk/resources"
        response_meta = requests.get(url_meta, headers=headers, params=params)
        if response_meta.status_code == 200:
            share_url = response_meta.json().get("public_url")
            return share_url
        else:
            raise DiskGetLinkError
    else:
        raise PublishingFileError


def main(user_upl_path, link: str):
    """Основная функция для загрузки и обработки видео."""
    logger.debug("youtube.main()")

    download_video(link, user_upl_path, COOKIES_FILE)
    video_name = get_video_name_from_uploads(user_upl_path, "mp4")

    yandex_disk_file_path = f"disk:/Приложения/{disk_app_folder_name}/{video_name}"
    upload_file_to_disk_folder(user_upl_path, video_name, "disk:/Приложения/bot_convert")

    share_url = get_file_shareable_link, yandex_disk_file_path
    return share_url
