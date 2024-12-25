class MyExeption(Exception):
    pass


class ServerError(MyExeption):
    """Класс ошибки со стороны сервера"""
    pass


class ClientError(MyExeption):
    """Класс ошибки со стороны клиента"""
    pass


class NoneError(MyExeption):
    """Класс ошибки пустого ответа"""
    pass


class FileFormatError(MyExeption):
    """Класс ошибки расширения файла"""
    pass
