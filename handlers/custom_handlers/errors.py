import os
from loader import bot

uploads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))


def handle_error(message, error_code):
    """Обработчик ошибок с завершением состояния и удалением файла."""
    clearing_uploads()
    bot.set_state(message.from_user.id, None, message.chat.id)
    bot.send_message(message.chat.id,
                     f"‼️Ошибка ({error_code})‼️")


def clearing_uploads():
    """
    Удаляет все загруженные пользователем файлы.
    :return:
    """
    try:
        for filename in os.listdir(uploads_path):
            file_path = os.path.join(uploads_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Ошибка при удалении файла: {e}")
                return False
    except Exception:
        return False
