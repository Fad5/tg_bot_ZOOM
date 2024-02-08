class TxtHandler:
    """
    Клас предназначен для работы с файлами txt формата

    Методы:
    - txt_read - Функция для чтения txt файлов
    - txt_write -  Функция для записи  txt файлов
    - txt_add -  Функция для добавления данных в txt файл
    """

    @staticmethod
    def txt_read(path: str, encoding: str = 'utf-8') -> str:
        """
        Функция для чтения txt файлов

        - path - путь к файлу
        - encoding - кодировка 
        return: data
        """
        with open(path, 'r', encoding=encoding) as file:
            data = file.read()
            return data

    @staticmethod
    def txt_write(data: str, path: str, encoding: str = 'utf-8') -> None:
        """
        Функция для записи  txt файлов

        - data - данные для записи 
        - path - путь к файлу
        - encoding - кодировка 
        return: None
        """
        with open(path, 'w', encoding=encoding) as file:
            file.write(data)

    @staticmethod
    def txt_add(data: str, path: str, encoding: str = 'utf-8') -> None:
        """
        Функция для добавления данных в txt файл

        - data - данные для записи
        - path - путь к файлу
        - encoding - кодировка 
        return: None
        """
        with open(path, 'a', encoding=encoding) as file:
            file.write(data)
