import datetime
import pandas as pd
import threading
from Work_with_file import TxtHandler


def create_cvs_file() -> None:
    """
    Функция забирает онлайн таблицу google, проходится pandas и создает csv с данными
    :return: None
    """
    df = pd.read_csv(
        'https://docs.google.com/spreadsheets/d/1vZc0LfpNmLZKnvn4EiEeD-HTZE5UJ2wBZX5fOF6FtBk/export?format=csv')
    
    column_names = df.keys().tolist()
    print(column_names)

    new_df = df[
        [column_names[0], column_names[1], column_names[2], column_names[3],column_names[4], column_names[5], column_names[6], column_names[7], column_names[8],
         column_names[9], column_names[10], column_names[11], column_names[12], column_names[13],
         column_names[14]]]  # Выберем из датафрейма  столбцы и сохраним в новый датафрейм
    new_df.to_csv('data_base.csv', index=False)  # Экспорт в CSV файл
    info = 'Succusfull '+ str(datetime.datetime.now())
    print(info)
    TxtHandler.txt_write(info,'report_parsing.txt')
    threading.Timer(3600, create_cvs_file).start()