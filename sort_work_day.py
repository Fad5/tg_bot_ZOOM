import datetime
import pandas as pd
import threading


def create_cvs_file() -> None:
    """
    Функция забирает онлайн таблицу google, проходится pandas и создает csv с данными
    :return: None
    """
    df = pd.read_csv(
        'https://docs.google.com/spreadsheets/d/1vZc0LfpNmLZKnvn4EiEeD-HTZE5UJ2wBZX5fOF6FtBk/export?format=csv')
    new_df = df[
        ['Группа', 'Программа', 'Поток или модуль', 'Дата', 'Время', 'Часы', 'Предмет', 'Преподаватель', 'Комментарий',
         'Примечание', 'Аудитория', 'Ссылка на вебинар', 'Ссылка на запись', 'Оператор',
         'аккаунт']]  # Выберем из датафрейма 2 столбца и сохраним в новый датафрейм
    new_df.to_csv('data_base.csv', index=False)  # Экспорт в CSV файл
    print('Succusfull', datetime.datetime.now())
    threading.Timer(3600, create_cvs_file).start()