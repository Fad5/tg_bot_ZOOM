import csv
import datetime
from value_sort import days
from config import invalid_link_to_post
from typing import Any


def formatting_noted(txt: str) -> str:
    """
    Функция, которая отображать заметки

    - txt - заметка 
    return: txt - отформатированная заметка 
    """
    if txt in invalid_link_to_post:
        return 'Нет'
    else:
        formatting_txt = txt.replace('\n', ' ')
        return formatting_txt


def date_formatting(txt: str) -> str:
    """
    Преобразовывает доту из YY.MM.DD в YY-MM-DD, 
    если строка пуста, то пропускаем
    :param txt:
    :return:
    """
    if ' ' in txt:
        return ''
    if txt not in invalid_link_to_post:
        date_list = txt.replace('\n', ' ').replace(',', '.').split('.')
        date_datetime = date_list[2] + '-' + date_list[1] + '-' + date_list[0]
        return date_datetime
    else:
        return ''


def from_watch_in_hours(element: str) -> float | None:
    """
    Функция принимает переменную (XX.XX-XX.XX) типа str, обрабатываем значение(меняем '.' на ':', меняем ',' на '.'),
    разделяет методом split по знаку "-", (XX:XX, XX:XX), получаем сумму минут от первого и второго значнеие,
    находим разницу и возвращаем это значение
    """
    print(element)
    if element == '':
        return None
    else:
        element = str(element).replace(' ', '')
        formatting_element = (element.replace('.', ':').replace('.', ':')
                              .replace(' ', '').replace(',', '.')).replace(
            '—', '-').replace('–', '-').replace("−", '-')
        formatting_elements = formatting_element.replace('.', ':').split('-')
        fist_time = formatting_elements[0].find(':')
        second_time = formatting_elements[1].find(':')
        start_time = int(formatting_elements[0][:fist_time]) * 60 + int(formatting_elements[0][fist_time + 1:])
        finish_time = int(formatting_elements[1][:second_time]) * 60 + int(formatting_elements[1][second_time + 1:])
        summa_hours = finish_time - start_time
        result = float(summa_hours / 60)
        return result


def get_info_work_day(user) -> list[dict[str | Any, str | Any]]:
    """
    Функция, которая получает имя пользователя и потом проходиься по
    csv файлу и помещает в js файл
    :param user: как записан в exel файле 
    :return:
    """
    name_file = 'data_base'
    js = []
    user_name_list = user.split('|')
    with open(f'{name_file}.csv', newline='', encoding='utf-8') as File:
        reader = csv.reader(File)
        for row in reader:
            for user_name in user_name_list:
                if user_name in row:
                    js.append({
                        '#': row[0].replace('\n', ' '),
                        'Program': row[1].replace('\n', ' '),
                        'Modul': row[2].replace('\n', ' '),
                        'Data': date_formatting(row[3]),
                        'Time': row[4].replace(' ', '').replace('.', ':'),
                        'Watch': row[5].replace('\n', ' '),
                        'Item': row[6].replace('\n', ' '),
                        'Comment': row[8].replace('\n', ' '),
                        'Teacher': row[7].replace('\n', ' '),
                        'Note': formatting_noted(row[9]),
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
    Функция проходится по файлу csv и получит дату, если дата совпадает с заданной в argument,
    то мы получим этот элемент преобразовываем и помещаем в переменную description и возвращаем
    :param work_day:
    :param argument:
    :param day_read:
    :return:
    """
    if work_day['Data'] not in invalid_link_to_post:
        date_json = work_day['Data']
        data_sort = datetime.datetime.strptime(date_json, '%Y-%m-%d').date()
        if data_sort == days(argument, day=day_read):
            description_for_show_work_day = (
                f"🎓 Программа: {work_day['Program']} \n📗Предмет: {work_day['Item']}\n👨‍🏫Преподаватель:"
                f" {work_day['Teacher']}\n🗓Дата: "
                f"{work_day['Data']}\n🕐Время: {work_day['Time']}\n❗Примечание: {work_day['Note']}\n📌Оператор:"
                f" {work_day['Operator']}\n🔒Аккаунт: {work_day['Account']}.")
            return description_for_show_work_day
    else:
        pass


def read_js_day(work_day: dict, date_base_day: list):
    """
    Функция проходится по файлу csv и получит дату, если дата совпадает с заданной в work_day и есть в date_base_day,
    то мы получим этот элемент преобразовываем и помещаем в переменную discription и возвращаем
    :param work_day:
    :param date_base_day:
    :return:
    """
    if work_day['Data'] not in invalid_link_to_post:
        date_json = work_day['Data']
        data_sort = datetime.datetime.strptime(date_json, '%Y-%m-%d').date()
        if data_sort in date_base_day:
            description = (
                f"🎓Программа: {work_day['Program']} \n📗Предмет: {work_day['Item']}\n👨‍🏫Преподаватель:"
                f" {work_day['Teacher']}\n🗓Дата: "
                f"{work_day['Data']}\n🕐Время: {work_day['Time']} \n❗Примечание: {work_day['Note']} "
                f"\n📌Оператор: {work_day['Operator']}\n🔒Аккаунт: {work_day['Account']}.")
            return description
    else:
        pass


def read_js_hours(work_day: dict, date_base_day: list):
    """
    Функция проходится по файлу csv и получает дату, если дата совпадает с заданной в work_day и есть в date_base_day,
    то мы получим этот элемент преобразовываем и помещаем в переменную discription и возвращаем
    :param work_day:
    :param date_base_day:
    :return:
    """
    if work_day['Data'] not in invalid_link_to_post:
        date_json = work_day['Data']
        data_sort = datetime.datetime.strptime(date_json, '%Y-%m-%d').date()
        if data_sort in date_base_day:
            if work_day['Link to post'][:27] == invalid_link_to_post:
                if work_day['Hours'] == None:
                    pass
                else:
                    hours = work_day['Hours']
                    print_hours_day = f'🗓 {work_day["Data"]}    🕰 {str("%.2f" % work_day["Hours"])}\n'
                    return hours, print_hours_day
            else:
                pass
    else:
        pass
