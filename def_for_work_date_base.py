import sqlite3

file_db = 'server.db'


def add_user_db(id_tg: int, name_user: str, table: str = 'user'):
    """
    Добавление пользователя в базу данных
    :param table: название таблицы в которую будем вносить изменения
    :param id_tg: id telegram аккаунта
    :param name_user: имя в exel таблице
    :return: None
    """
    result = is_user(id_tg=id_tg, table=table)
    if not result:
        db = sqlite3.connect(file_db)
        sql = db.cursor()
        sql_add = f"""INSERT INTO {table}(id_TG,user_name) VALUES (?,?)"""
        date = (id_tg, name_user)
        sql.execute(sql_add, date)
        db.commit()
        db.close()
        return True
    else:
        return False


def del_user_db(id_tg: int, table: str = 'user'):
    """
    Удаление пользователя из базы данных
    :param table: название таблицы в которую будем вносить изменения
    :param id_tg: id telegram аккаунта
    :return: None
    """
    db = sqlite3.connect(file_db)
    sql = db.cursor()
    sql.execute(f"""DELETE FROM {table} WHERE id_TG =={id_tg}""")
    db.commit()
    db.close()


def update_user_db(argument_replace: str or int, new_argument: str or int, tg_id: int, table: str = 'user'):
    """
    Обновление данных
    :param table: таблица в которую будем вносить изменения
    :param argument_replace: значение которе нужно поменять
    :param new_argument: новое значение
    :param tg_id: выбирает строку для замены
    :return: None
    """
    db = sqlite3.connect(file_db)
    sql = db.cursor()
    sql_update = f"""UPDATE {table} SET {argument_replace} = ? WHERE id_TG = ? """
    date = (new_argument, tg_id)
    sql.execute(sql_update, date)
    db.commit()
    db.close()


def show_db(table: str, message='') -> list:
    db = sqlite3.connect(file_db)
    sql = db.cursor()
    sql.execute(f"""SELECT *  FROM {table} WHERE id_TG !=''""")
    for i in sql:
        message = message + f'▪️ id: <code>{i[0]}</code>  name: {i[1]}\n'
    return message


def is_user(id_tg: int, table: str = 'user') -> bool:
    """
    Функция получает id_tg и проходится по базе данных собирает в один список,
    проверяет есть ли этот id, если есть возвращает True
    :param table: таблица в которую будем вносить изменения
    :param id_tg: id аккаунта telegram
    :return: bool (True, False)
    """
    db = sqlite3.connect(file_db)
    sql = db.cursor()
    sql.execute(f"""SELECT id_TG FROM {table} WHERE id_TG !=''""")
    list_id = []
    for id_ in sql:
        id_ = id_[0]
        list_id.append(id_)
    if id_tg in list_id:
        return True
    else:
        return False


def get_user_name(id_tg: int, table: str = 'user'):
    """
    Получения user_name из базы данных

    - id_tg - id телеграмма
    - file_db - база данных
    - table - таблица от куда будем брать информацию 
    return: user_name 
    """
    db = sqlite3.connect(file_db)
    sql = db.cursor()
    sql.execute(f"""SELECT user_name FROM {table} WHERE id_TG =={id_tg}""")
    for i in sql:
        user_name = i
        return user_name[0]


def show_table() -> list:
    """
    Функция для отображения таблиц в базе данных

    - file_db - база данных
    return: list_database - cписок таблиц которые есть в бд
    """
    db = sqlite3.connect(file_db)
    sql = db.cursor()
    list_database = []
    sql.execute("""select * from sqlite_master
            where type = 'table'""")
    tables = sql.fetchall()
    for table in tables:
        list_database.append(table[1])
    return list_database
