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

```bash
docker build -t bot_convert:latest . && docker run --name bot_convert --restart unless-stopped -d bot_convert:latest
```
