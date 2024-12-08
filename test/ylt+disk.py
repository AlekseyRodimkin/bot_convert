import yt_dlp
import sys
import subprocess
import requests
import os
from dotenv import load_dotenv
import json

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()
TOKEN = os.getenv("YANDEX_DISK_TOKEN")
url = "https://youtu.be/nxiJQk-sfDo"
output_dir = "./downloads"
cookies_file = "./cookies.txt"


def get_video_name(directory):
    """
    Проходит по указанной директории и выводит полные имена файлов с расширением .mp4.

    Параметры:
    directory (str): Директория для поиска файлов.

    Возвращает:
    list: Список полных путей к файлам с расширением .mp4.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp4"):
                # full_path = os.path.join(root, file)
                return file


def download_video(url, output_dir, cookies_file):
    # Путь для выходного видеофайла
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    # Команда yt-dlp для загрузки видео mkv с использованием cookies
    command_mkv = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio/best",  # Выбор лучшего видео и аудио
        "--merge-output-format", "mkv",  # Сохранение в MKV
        "-o", output_template,  # Шаблон имени файла
        "--write-info-json",  # Сохранение метаданных
        "--cookies", cookies_file,  # Передача cookies для аутентификации
        url
    ]

    command_mp4 = ["yt-dlp",
                   "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",  # Выбор лучшего видео и аудио
                   "--merge-output-format", "mp4",  # Сохранение в MP4
                   "-o", output_template,  # Шаблон имени файла
                   "--write-info-json",  # Сохранение метаданных
                   "--cookies", cookies_file,  # Передача cookies для аутентификации url
                   url
                   ]

    print("Загружается видео...")
    # subprocess.run(command_mkv, check=True)
    subprocess.run(command_mp4, check=True)
    print("Видео успешно загружено.")

    # Находим JSON файл с метаданными
    info_json_path = next(
        (os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".info.json")), None
    )
    if not info_json_path:
        raise FileNotFoundError("Файл метаданных .info.json не найден.")

    return info_json_path


def create_kodi_friendly_files(info_json_path):
    # Читаем данные из JSON файла
    with open(info_json_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    title = metadata.get("title", "Без названия")
    description = metadata.get("description", "Нет описания")
    thumbnail = metadata.get("thumbnail", "")

    # Путь к базовым файлам (без расширений)
    base_path = os.path.splitext(info_json_path)[0].replace(".info", "")

    # Загружаем обложку, если доступна
    cover_path = f"{base_path}-fanart.jpg"
    if thumbnail:
        with open(cover_path, "wb") as f:
            f.write(requests.get(thumbnail).content)
        print(f"Обложка сохранена: {cover_path}")
    else:
        print("Обложка не найдена.")

    # Создаем содержимое .nfo файла
    nfo_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<movie>
    <title>{title}</title>
    <plot>{description}</plot>
    <thumb>{cover_path}</thumb>
</movie>
"""

    # Сохраняем .nfo файл
    nfo_path = f"{base_path}.nfo"
    with open(nfo_path, "w", encoding="utf-8") as nfo_file:
        nfo_file.write(nfo_content)

    print(f".nfo файл успешно создан: {nfo_path}")


def upload_file_to_disk_folder(file_name, folder_path):
    """Функция для загрузки на диск"""
    url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {"Authorization": f"OAuth {TOKEN}"}
    params = {"path": f"{folder_path}/{file_name}", "overwrite": "true"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        upload_url = response.json()["href"]
        with open(f"{output_dir}/{file_name}", "rb") as f:
            print('Начинаю загрузку файла на диск')
            upload_response = requests.put(upload_url, files={"file": f})
            if upload_response.status_code == 201:
                print(f"Файл {file_name} успешно загружен в {folder_path}.")
            else:
                print(f"Ошибка загрузки файла: {upload_response.json()}")
    else:
        print(f"Ошибка получения ссылки для загрузки: {response.json()}")


def get_file_shareable_link(file_path):
    """Функция публикации файла и получение публичной ссылки"""
    url_publish = "https://cloud-api.yandex.net/v1/disk/resources/publish"
    headers = {"Authorization": f"OAuth {TOKEN}"}
    params = {"path": file_path}

    # Публикуем файл
    response = requests.put(url_publish, headers=headers, params=params)
    if response.status_code == 200:
        # Получаем публичную ссылку
        url_meta = "https://cloud-api.yandex.net/v1/disk/resources"
        response_meta = requests.get(url_meta, headers=headers, params=params)
        if response_meta.status_code == 200:
            share_url = response_meta.json().get("public_url")
            print(f"Публичная ссылка на файл: {share_url}")
            return share_url
        else:
            print(f"Ошибка получения ссылки на файл: {response_meta.json()}")
    else:
        print(f"Ошибка публикации файла: {response.json()}")


def main():
    os.makedirs(output_dir, exist_ok=True)

    try:
        # info_json_path = download_video(url, output_dir, cookies_file)
        # create_kodi_friendly_files(info_json_path)

        # with open(info_json_path, "r", encoding="utf-8") as f:
        #     metadata = json.load(f)

        # title = metadata.get("title", "Без названия")
        # local_file_path = "video.mkv"  # Локальный файл

        title = get_video_name(output_dir)
        print(title)
        yandex_disk_file_path = f"disk:/Приложения/bot_convert"  # Путь на Яндекс.Диске

        upload_file_to_disk_folder(title, yandex_disk_file_path)

        get_file_shareable_link(f"{yandex_disk_file_path}/{title}")



    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
