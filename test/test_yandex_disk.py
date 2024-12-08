import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()
TOKEN = os.getenv("YANDEX_DISK_TOKEN")


def upload_file_to_folder(file_path, folder_path):
    """Функция для загрузки на диск"""
    url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {"Authorization": f"OAuth {TOKEN}"}
    params = {"path": f"{folder_path}/{file_path}", "overwrite": "true"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        upload_url = response.json()["href"]
        with open(file_path, "rb") as f:
            upload_response = requests.put(upload_url, files={"file": f})
            if upload_response.status_code == 201:
                print(f"Файл {file_path} успешно загружен в {folder_path}.")
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



local_file_path = "1.jpeg"  # Локальный файл
yandex_disk_file_path = f"disk:/Приложения/bot_convert"  # Путь на Яндекс.Диске
upload_file_to_folder(local_file_path, yandex_disk_file_path)
get_file_shareable_link(f"{yandex_disk_file_path}/{local_file_path}")

# Итоговая схема работы
# Бот получает видео от пользователя.
# Файл загружается в общую папку с уникальным именем.
# После загрузки создаётся публичная ссылка на файл.
# Пользователь получает ссылку только на свой файл.


# удааление файла (сообщить пользователю что файл будет доступен 24 часа)
# . Использование системного планировщика задач (Linux/Windows)
# Linux (cron):

# Сохраняем скрипт в файл, например delete_file.py.
# Настраиваем cron для запуска в нужное время.
# bash
# Копировать код
# crontab -e
# Добавляем строку:
# bash
# Копировать код
# 0 14 * * * /usr/bin/python3 /path/to/delete_file.py
# Это запускает скрипт каждый день в 14:00.
# Windows (Task Scheduler):
#
# В Планировщике задач создайте задачу, которая запускает Python-интерпретатор с вашим скриптом.
# Этот подход не требует постоянного выполнения Python-программы.
