# Синхронный Telegram-бот

- 🌐 Telegram: [not_file_bot](https://t.me/not_file_bot)

## Функции

- **Конвертация PDF в DOCX**
- **Создание аудио из PDF**
- **Создание аудио из текста**
- **Создание изображения из текста**
- **Конвертация изображений в черно-белый формат**
- **Конвертация изображений из JPG в PNG**
- **Добавление шума на изображение**
- **Генерация 12-значного штрих-кода**
- **Генерация QR-кода для ссылок, текста или контактных данных**
- **Получение кода HTML-страницы**
- **Получение информации об IP**

# Установка

### Клонирование репозитория

```bash
git clone https://github.com/your-username/bot_convert.git
cd bot_convert
```

### Настройка переменных окружения

Создайте файл `.env` в корневой папке проекта, скопировав `.env.template`, и добавьте свой Telegram API токен:

```text
TELEGRAM_TOKEN=your_telegram_bot_token
```

## 1. Обычная установка

### 1.1 Создание виртуального окружения (рекомендуется)

```bash
python -m venv .venv
source .venv/bin/activate  # Для Windows: .venv\Scripts\activate
```

### 1.2 Установка зависимостей

```bash
pip install -r requirements.txt
```

### 1.3 Запуск бота

```bash
python main.py
```

---

## 2. Установка через Docker

### 2.1 Сборка и запуск контейнера

```bash
docker build -t bot_convert_app .
docker run bot_convert_app
```

---

## Зависимости

Проект использует следующие библиотеки:

- `pyTelegramBotAPI` — для взаимодействия с Telegram API
- `python-docx` — для работы с DOCX файлами
- `Pillow` — для работы с изображениями
- `pdf2docx` — для конвертации PDF в DOCX
- `python-barcode` — для генерации штрих-кода
- `qrcode` — для генерации QR-кода
- `pdfplumber`, `gtts` — для создания аудио

<img src="https://github.com/AlekseyRodimkin/bot_convert/raw/main/README_images/qr.png" width="300">
