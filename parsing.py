import csv
import datetime
from value_sort import days


def date_formating(txt):
    """
    Преобразовывает доту из YY.MM.DD в YY-MM-DD
    :param txt:
    :return:
    """
    date_list = txt.replace('\n', ' ').replace(',', '.').split('.')
    date_datetime = date_list[2] + '-' + date_list[1] + '-' + date_list[0]
    return date_datetime


def from_watch_in_hours(element):
    if element == '':
        return 0
    else:
        formating_element = (element.replace(' ', '').replace('.', ':').replace(',', '.'))
        formating_element = formating_element.split('-')
        hours =  formating_element[0].find(':')
        minutes =  formating_element[1].find(':')
        summa_minutes = (int( formating_element[1][:minutes]) * 60 + int( formating_element[1][minutes + 1:]))
        - (int( formating_element[0][:hours]) * 60 + int( formating_element[0][hours + 1:]))
        summa_hours = summa_minutes / 60
        return summa_hours


def get_info_work_day(user):
    """
    Функция которя получает имя пользователя и потом проходиься по
    csv файлу и помещает в js файл
    :param user:
    :return:
    """
    name_file = 'data_base'
    js = []

    with open(f'{name_file}.csv', newline='', encoding='utf-8') as File:
        reader = csv.reader(File)
        for row in reader:
            if user in row:
                js.append({
                    '#': row[0].replace('\n', ' '),
                    'Programm': row[1].replace('\n', ' '),
                    'Modul': row[2].replace('\n', ' '),
                    'Data': date_formating(row[3]),
                    'Trowme': row[4].replace(' ', '').replace('.', ':'),
                    'Watch': row[5].replace('\n', ' '),
                    'Item': row[6].replace('\n', ' '),
                    'Comment': row[8].replace('\n', ' '),
                    'Teacher': row[7].replace('\n', ' '),
                    'Note': row[9].replace('\n', ' '),
                    'Audience': row[10].replace('\n', ' '),
                    'Webinar link': row[11].replace('\n', ' '),
                    'Link to post': row[12].replace('\n', ' '),
                    'Operator': row[13].replace('\n', ' '),
                    'Account': row[14].replace('\n', ' '),
                    'Hours': from_watch_in_hours(row[4])
                })
    return js


def read_js(work_day, argument, day_read=1):
    """
    Функция проходится по файлу csv и получет дату, если дата совпадает с заданой в argument,
    то мы получем этот элемент преобразовываем и помещаем в переменную discription и возвращаем
    :param work_day:
    :param argument:
    :param day_read:
    :return:
    """
    if work_day['Data'] == "":
        pass
    date_json = work_day['Data']
    data_sort = datetime.datetime.strptime(date_json, '%Y-%m-%d').date()
    if data_sort == days(argument, day=day_read):
        description_for_show_work_day = (f"🎓 Программа: {work_day['Programm']} \n\n📗Предмет: {work_day['Item']}\n👨‍🏫Преподаватель: {work_day['Teacher']}\n🗓Дата: "
                       f"{work_day['Data']}\n🕐Время: {work_day['Trowme']} \n📌Оператор: {work_day['Operator']}\n🔒Акаунт: {work_day['Account']}.")
        return description_for_show_work_day
    else:
        pass


def read_js_day(work_day:dict, date_base_day:list):
    """
    Функция проходится по файлу csv и получет дату, если дата совпадает с заданой в work_day и есть в date_base_day,
    то мы получем этот элемент преобразовываем и помещаем в переменную discription и возвращаем
    :param work_day:
    :param date_base_day:
    :return:
    """
    if work_day['Data'] == "":
        pass
    date_json = work_day['Data']
    data_sort = datetime.datetime.strptime(date_json, '%Y-%m-%d').date()
    if data_sort in date_base_day:
        description = (f"🎓Программа: {work_day['Programm']} \n📗Предмет: {work_day['Item']}\n👨‍🏫Преподаватель: {work_day['Teacher']}\n🗓Дата: "
                       f"{work_day['Data']}\n🕐Время: {work_day['Trowme']} \n📌Оператор: {work_day['Operator']}\n🔒Акаунт: {work_day['Account']}.")
        return description
    else:
        pass


def read_js_hours(work_day:dict, date_base_day:list):
    """
    Функция проходится по файлу csv и получет дату, если дата совпадает с заданой в work_day и есть в date_base_day,
    то мы получем этот элемент преобразовываем и помещаем в переменную discription и возвращаем
    :param work_day:
    :param date_base_day:
    :return:
    """
    if work_day['Data'] == "":
        pass
    date_json = work_day['Data']
    data_sort = datetime.datetime.strptime(date_json, '%Y-%m-%d').date()
    if data_sort in date_base_day:
        if work_day['Webinar link'] != "":
            if work_day['Link to post'] != "":
                hours = work_day['Hours']
                print_hours_day = f'🗓 {work_day["Data"]}    🕰 {str(work_day["Hours"])}\n'
                return hours, print_hours_day
            else:
                pass

