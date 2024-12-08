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


class DiskGetLinkError(MyExeption):
    """Класс ошибки получения ссылки для загрузки на диск"""
    pass


class PublishingFileError(MyExeption):
    """Класс ошибки публикации файла на диске"""
    pass


class FileDownloadError(MyExeption):
    """Класс ошибки загрузки файла на диск"""
    pass
