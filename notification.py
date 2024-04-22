from datetime import datetime

from def_for_work_date_base import show_db, show_db_notification
from parsing import get_info_work_day, read_js_notification, read_js

list_info = []
data = get_info_work_day('Андрей А')


def plus_hours(data_zoom):
    start_time = data_zoom.split('-')
    time_split = start_time[0].split(':')
    time = int(time_split[0]) - 1
    time = f'{time}:{time_split[1]}'
    return time


def hours_correct(data_zoom):
    zoom_time = plus_hours(data_zoom)
    time_now = str(datetime.now().time())
    time_now_correct = time_now.split(':')
    correct_now = f'{time_now_correct[0]}:{time_now_correct[1]}'
    if correct_now == zoom_time:
        return 'Запустить zoom через час'
    else:
        pass


users_is_notifications = show_db_notification('user')
print(users_is_notifications)


def now_date():
    now_datetime = datetime.now().date()
    return now_datetime


def data_(user_name):
    data_user = get_info_work_day(user_name)
    for i in data_user:
        data_sort = datetime.strptime(i['Data'], '%Y-%m-%d').date()
        if data_sort == now_date():
            list_info.append(i)
    return list_info


def get_hour_notification(user_name):
    for date_list in data_(user_name):
        zoom_time = plus_hours(date_list['Time'])
        time_now = str(datetime.now().time())
        time_now_correct = time_now.split(':')
        correct_now = f'{time_now_correct[0]}:{time_now_correct[1]}'
        if correct_now == zoom_time:
            return 'Запустить zoom через час'

