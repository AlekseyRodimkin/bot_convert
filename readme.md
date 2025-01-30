# Синхронный Telegram-бот

## Функции

- **Конвертация PDF в DOCX**
- **Создание аудио из PDF**
- **Создание аудио из текста**
- **Создание изображения из текста**
- **Конвертация изображений в черно-белый формат**
- **Конвертация изображений из JPG в PNG**
- **Добавление шума на изображение**
- **Генерация 12 значного штрих-кода**
- **Генерация QR кода для ссылок, текста или контактных данных**
- **Получение кода HTML страницы**
- **Получение информации об IP**

# Установка 1

### Клонирование репозитория:

```bash
git clone https://github.com/your-username/bot_convert.git
cd bot_convert
```

### Создание виртуального окружения (рекомендуется):

```bash
python -m venv .venv
source .venv/bin/activate  # Для Windows: .venv\Scripts\activate
```

### Установка зависимостей:

```bash
pip install -r requirements.txt
```

### Настройка переменных окружения:

Создайте файл .env в корневой папке проекта скопировав .env.template и добавьте свой Telegram API токен:

```text
TELEGRAM_TOKEN=your_telegram_bot_token
```

### Запуск бота:

```bash
python main.py
```

# Установка 2

### Клонирование репозитория:

```bash
git clone https://github.com/your-username/bot_convert.git
cd bot_convert
```

### Соберите и запустите Docker:

```bash
docker build -t bot_convert_app .
docker run bot_convert_app
```

## Зависимости

Проект использует следующие библиотеки:

- pyTelegramBotAPI — для взаимодействия с Telegram API
- python-docx — для работы с DOCX файлами
- Pillow — для работы с изображениями
- pdf2docx — для конвертации PDF в DOCX.
- python-barcode — для генерации штрих-кода
- qrcode - для генерации QR кода
- pdfplumber, gtts — создание аудио
