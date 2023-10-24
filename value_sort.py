from datetime import date, datetime
from datetime import timedelta


def start_weekday() -> date:
    current_day = date.today()
    week = current_day.weekday()
    start_week = current_day - timedelta(days=week)
    return start_week


def week(argument: str = '') -> tuple[date, date]:
    if argument == 'next':
        finish_week = start_weekday() + timedelta(days=13)
        start_week = start_weekday() + timedelta(days=7)
        return start_week, finish_week
    elif argument == 'last':
        finish_week = start_weekday() - timedelta(days=1)
        start_week = start_weekday() - timedelta(days=7)
        return start_week, finish_week
    else:
        current_day = date.today()
        week = current_day.weekday()
        start_week = current_day - timedelta(days=week)
        finish_week = start_weekday() + timedelta(days=6)
        return start_week, finish_week


def days(optional: str, day: int = 1, current_day: date = date.today()) -> date:
    if optional == 'next':
        next_day = current_day + timedelta(days=day)
        return next_day
    elif optional == 'last':
        last_day = current_day - timedelta(days=day)
        return last_day
    else:
        return current_day


def get_password_mail(zoom_account: str, ACCOUNTS: dict) -> str:
    if zoom_account in ACCOUNTS:
        data_account = ACCOUNTS[zoom_account]
        resault = (f'📬 Почта: <code>{data_account["mail"]}</code> \n🔑Пароль: <code>{data_account["password"]}</code>')
        return resault
    else:
        resault = "Нет данных"
        return resault


def week_name(argument: str = '') -> str:
    start_week = week(argument)[0]
    finish_week = week(argument)[1]
    resault = f'{start_week.day}.{start_week.month} - {finish_week.day}.{finish_week.month}'
    return resault


def name_week_button() -> list:
    arguments = ['last', '', 'next']
    list_week_date = []
    for argument_week in arguments:
        result = week_name(argument_week)
        list_week_date.append(result)
    return list_week_date


def list_work_day() -> list:
    full_list_day = []
    arguments = ['last', '', 'next']
    for argument in arguments:
        data = week(argument)
        start_week = data[0]
        list_day = []
        for i in range(0, 7):
            number_day = days('next', current_day=start_week, day=i)
            list_day.append(number_day)
        full_list_day.append(list_day)
    return full_list_day


def zero_error(element: int):
    if element == 0:
        return 12
    if 13 > element >= 1:
        return element
    else:
        return None


def create_list_date_hours(current_day: date, starting_point: date):
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
    date_current = date.today()
    date_current_str = str(date_current)
    check_10 = date_current_str[:8] + '10'
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


def check_hours_month(argument):
    if argument == 'last_list_hours':
        date_current = date.today()
        day_in = date.today().day
        day_in_day = day_in - 1
        finish_seathe = date_current - timedelta(days=day_in_day + 1)
        finish_month = finish_seathe.month
        finish_year = finish_seathe.year
        get_last_month = f'{str(finish_year)}-{str(finish_month)}-01'
        finish_datetime = datetime.strptime(get_last_month, '%Y-%m-%d').date()
        start_current_month = date_current - timedelta(days=day_in_day)
        list_day_in_month_last = create_list_date_hours(current_day=start_current_month, starting_point=finish_datetime)
        return list_day_in_month_last
    if argument == 'current_list_hours':
        date_current = date.today()
        day_in = date.today().day
        day_in = day_in - 1
        start_current_month = date_current - timedelta(days=day_in)
        list_day_in_month_current = (
            create_list_date_hours(current_day=date_current, starting_point=start_current_month))
        return list_day_in_month_current