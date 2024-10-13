# Telegram-бот для работы с файлами и изображениями

## Функции

- **Конвертация PDF в DOCX**
- **Конвертация изображений в черно-белый формат**
- **Добавление шума на изображение**
- **Удаление фона с изображений**
- **Генерация штрих-кода**
- **Получение кода HTML страницы**

## Установка

Для запуска Telegram-бота вам потребуется Python 3.x и установленные зависимости. Следуйте шагам ниже:

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
## Зависимости
Проект использует следующие библиотеки:
- pyTelegramBotAPI — для взаимодействия с Telegram API.
- python-docx — для работы с DOCX файлами.
- Pillow — для обработки изображений.
- pdf2docx — для конвертации PDF в DOCX.
- python-barcode — для генерации штрих-кода
- python-barcode — для генерации штрих-кода
- OpenCV — удаление фона с изображений