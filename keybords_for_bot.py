from aiogram import types


def get_kb_list_db() -> types.ReplyKeyboardMarkup:
    """
    Функция будет выполнятся в машине состояний StatesdataBase
    """
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton('Показать список DataBase'))
    kb.add(types.KeyboardButton('Отмена'))
    return kb


def get_kb_start() -> types.ReplyKeyboardMarkup:
    """
    Главная таблица которая будет отображаться при запуске бота
    """
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton('Последнее обновление'))
    kb.add(types.KeyboardButton('Операторы Webinar.ru'))
    kb.add(types.KeyboardButton('Аккаунты zoom'))
    return kb
