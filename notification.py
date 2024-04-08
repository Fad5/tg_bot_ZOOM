from datetime import datetime

from def_for_work_date_base import show_db, show_db_notification
from parsing import get_info_work_day, read_js_notification

list_info = []
data = get_info_work_day('Андрей А')


def get_data(data_zoom):
    for i in data_zoom:
        info = read_js_notification(work_day=i, argument='')
        if info is not None:
            list_info.append(info)
    return list_info[0][1]


def plus_hours(data_zoom):
    date = get_data(data_zoom)
    start_time = date.split('-')
    time_split = start_time[0].split(':')
    time = int(time_split[0]) + 1
    time = f'{time}:{time_split[1]}'
    return time


def hours_correct(data_zoom):
    zoom_time = plus_hours(data_zoom)
    time_now = str(datetime.now().time())
    time_now_correct = time_now.split(':')
    correct_now = f'{time_now_correct[0]}:{time_now_correct[1]}'
    if correct_now == zoom_time:
        return 'Запустить zoom через час'


users_is_notifications = show_db_notification('user')


for i in users_is_notifications:
    user_name = i[1]
    user_id = i[0]
