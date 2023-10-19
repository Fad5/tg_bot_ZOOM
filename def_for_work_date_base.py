import sqlite3

file_db = 'server.db'


def add_user_db(id_tg: int, name_user: str, database:str='user'):
    """
    Добавление пользователя в базу данных
    :param id_tg:
    :param name_user:
    :return:
    """
    result = is_user(id_tg=id_tg, database=database)
    if result == False:
        db = sqlite3.connect(file_db)
        sql = db.cursor()
        sql_add = (f"""INSERT INTO {database}(id_TG,user_name) VALUES (?,?)""")
        date = (id_tg, name_user)
        sql.execute(sql_add, date)
        db.commit()
        db.close()
        return True
    else:
        return False


def del_user_db(id_tg: int,database:str='user') -> None:
    """
    Удаление пользователя из базы данных
    :param id_tg:
    :return:
    """
    db = sqlite3.connect(file_db)
    sql = db.cursor()
    sql.execute(f"""DELETE FROM {database} WHERE id_TG =={id_tg}""")
    db.commit()
    db.close()


def update_user_db(argument_replace: str or int, new_argument: str or int, tg_id: int,database:str='user') -> None:
    """
    Обнавление данных
    :param argument_replace: значение которе нужно поменять
    :param new_argument: новое значение
    :param tg_id: вибирает строску для замены
    :return:
    """
    db = sqlite3.connect(file_db)
    sql = db.cursor()
    sql_update = (f"""UPDATE {database} SET {argument_replace} = ? WHERE id_TG = ? """)
    date = (new_argument, tg_id)
    sql.execute(sql_update, date)
    db.commit()
    db.close()


def show_db(database:str, message = '') -> list:
    db = sqlite3.connect(file_db)
    sql = db.cursor()
    sql.execute(f"""SELECT *  FROM {database} WHERE id_TG !=''""")
    for i in sql:
        message = message  + f'▪️ id: <code>{i[0]}</code>  name: {i[1]}\n'
    return message


def is_user(id_tg: int,database:str='user') -> bool:
    """
    Функция получает id_tg и проходится по базе данных собирает в один список,
    проверяет есть ли этот id, если есть возвращает True
    :param id_tg:
    :return:
    """
    db = sqlite3.connect(file_db)
    sql = db.cursor()
    sql.execute(f"""SELECT id_TG FROM {database} WHERE id_TG !=''""")
    list_id = []
    for id_ in sql:
        id_ = id_[0]
        list_id.append(id_)
    if id_tg in list_id:
        return True
    else:
        return False

def get_user_name(id_tg: int,database:str='user')->str:
    db = sqlite3.connect(file_db)
    sql = db.cursor()
    sql.execute(f"""SELECT user_name FROM {database} WHERE id_TG =={id_tg}""")
    for i in sql:
        user_name = i
        return user_name[0]

