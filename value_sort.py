from datetime import date, datetime, timedelta
from typing import List, Dict


def create_file_report(data) -> None:
    """
    Добавления в файл report_date.txt отчет о обновления exel файла

    return: None
    """
    with open('report_date.txt', 'a', encoding='utf-8') as f:
        f.write(data)


def start_weekday() -> date:
    """
    Функция, которая возвращает дату текущего понедельника

    return: start_week - дата текущего понедельника
    """
    current_day = date.today()
    weeks = current_day.weekday()
    start_week = current_day - timedelta(days=weeks)
    return start_week


def week(argument: str) -> tuple[date, date]:
    """
    Функция возвращает начало и конец недели в зависимости от argument,
    она работает с текущей, прошлой и будущей. Функйия получит начало этой недели
    и уже либо прибавляет 7 дней или убавляет для нахождения начало прошлой или будущей.

    - argument - ключ слова для получения значения(next, last, current)

    return: start_week, finish_week - (datetime.date(year, month, day), datetime.date(year, month, day))
    """
    data_kay = {'next': [13, 7], 'last': [1, 7], 'current': [0, 6]}
    current_day = date.today()
    weeks = current_day.weekday()
    start_week = current_day - timedelta(days=weeks)
    finish_week = start_week + timedelta(days=data_kay[argument][0])
    start_week = start_weekday() + timedelta(days=data_kay[argument][1])
    return start_week, finish_week


def days(argument: str, day: int = 1, current_day: date = date.today()) -> date:
    """
    Функция для получения даты текущего, прошлого и будующего дня в формате
    datetime.date в зависимости от argument

    - argument - (next, last,' ') - получение дня в зависимости от того что написано

    return: datetime.date 
    """
    create_file_report(f'{current_day} | {datetime.now()} \n')
    if argument == 'next':
        next_day = date.today() + timedelta(days=day)
        return next_day
    elif argument == 'last':
        last_day = date.today() - timedelta(days=day)
        return last_day
    else:
        return date.today()


def days_for_week(argument: str, day: int = 1, current_day: date = date.today()) -> date:
    """
    Получение текущего, прошлого и будующего дня в формате datetime,
    в зависимости от argument

    return: день в формате datetime ()
    """
    if argument == 'next':
        next_day = current_day + timedelta(days=day)
        return next_day
    elif argument == 'last':
        last_day = current_day - timedelta(days=day)
        return last_day
    else:
        return current_day


def get_password_mail(zoom_account: str, ACCOUNTS: Dict) -> str:
    """
    Получаем данные об аккаунте 

    - zoom_account - name в файле accounts_example.py
    - ACCOUNTS -  словари(ACCOUNTS_WEBINAR, ACCOUNTS_ZOOM) в файле accounts_example.py

    return result: Данные об аккаунте 
    """
    if zoom_account in ACCOUNTS:
        data_account = ACCOUNTS[zoom_account]
        result = f'📬 Почта: <code>{data_account["mail"]}</code> \n🔑Пароль: <code>{data_account["password"]}</code>'
        return result
    else:
        result = "Нет данных"
        return result


def list_work_day() -> List:
    """
    Функция создает список в который будут входить 3 спиcка состоящие из
    дней недели текущей, будущей и прошлой

    return: список список дней текущей, будущей и прошлой недели
      [[last_week_days],[current_week_days],[next_week_days]]
    """

    full_list_day = []
    arguments = ['last', 'current', 'next']
    for argument in arguments:
        data = week(argument)
        start_week = data[0]
        list_day = []
        for i in range(0, 7):
            number_day = days_for_week('next', current_day=start_week, day=i)
            list_day.append(number_day)
        full_list_day.append(list_day)
    return full_list_day


def zero_error(number_of_the_month: int) -> int | None:
    """
    Функция для корректного отображения номер месяца

    - number_of_the_month - номер месяца 
    """
    if number_of_the_month == 0:
        return 12
    if 13 > number_of_the_month >= 1:
        return number_of_the_month
    else:
        return None


def create_list_date_hours(current_day: date, starting_point: date):
    """
    Функция проходится циклом и от current_day(текущего дня) отнимается 1 день,
    до тех пор пока current_day == starting_point 

    return list_date: Получение дней с 10 по 10
    """
    list_date = []
    if current_day > starting_point:
        while current_day > starting_point:
            current_day = current_day - timedelta(days=1)
            list_date.append(current_day)
        return list_date
    if current_day < starting_point:
        while current_day > starting_point:
            current_day = current_day - timedelta(days=1)
            list_date.append(current_day)
        return list_date


def check_hours():
    """
    Получение дней с 10 по 10
    """
    # Получаем текущую дату
    date_current = date.today()
    # Преобразовываем в str date_current
    date_current_str = str(date_current)
    # Получаем year-month-10
    check_10 = date_current_str[:8] + '10'
    # Переводим в check_10 в datetime
    check_10_check = datetime.strptime(check_10, '%Y-%m-%d').date()
    if date_current > check_10_check:
        list_date_hours = (create_list_date_hours(current_day=date_current, starting_point=check_10_check))
        return list_date_hours
    if date_current < check_10_check:
        i = int(check_10_check.month) - 1
        i = zero_error(i)
        check_10_check_1 = check_10[:5] + str(i) + check_10[7:]
        check_10_check11 = datetime.strptime(check_10_check_1, '%Y-%m-%d').date()
        list_date_hours = (create_list_date_hours(current_day=date_current, starting_point=check_10_check11))
        return list_date_hours


check_hours()


def check_hours_month(argument: str):
    """
    Функция возвращает все дни в формате datetime.date

    - argument - 2 ключа: last_list_hours - список прошлого месяца,
        current_list_hours - список текущего месяца
    """
    if argument == 'last_list_hours':
        # Получаем текущую дату
        date_current = date.today()
        # Забираем только день
        day_in = date.today().day
        # Вычитаем 1 для получения начало текущего месяца 
        day_in_day = day_in - 1
        # Получаем конец прошлого месяца
        finish_date = date_current - timedelta(days=day_in_day + 1)
        # Получаем месяц
        finish_month = finish_date.month
        # Получаем год
        finish_year = finish_date.year
        # Создаем дату начало прошлого месяца
        get_last_month = f'{str(finish_year)}-{str(finish_month)}-01'
        # Из str в datetime.date переводим
        finish_datetime = datetime.strptime(get_last_month, '%Y-%m-%d').date()
        # Получаем начало текущего месяца
        start_current_month = date_current - timedelta(days=day_in_day)
        # Получаем в списке все дни прошлого месяца в формате [datetime.date(year, month, day),
        # datetime.date(year, month, day)]
        list_day_in_month_last = create_list_date_hours(current_day=start_current_month, starting_point=finish_datetime)
        return list_day_in_month_last
    if argument == 'current_list_hours':
        # Получаем текущую дату
        date_current = date.today()
        # Забираем только день
        day_in = date.today().day
        # Вычитаем 1 для получения начало текущего месяца
        day_in = day_in - 1
        # Получаем начало текущего месяца
        start_current_month = date_current - timedelta(days=day_in)
        # Получаем в списке все дни текущего месяца в формате [datetime.date(year, month, day),
        # datetime.date(year, month, day)]
        list_day_in_month_current = (
            create_list_date_hours(current_day=date_current, starting_point=start_current_month))
        return list_day_in_month_current
