import csv
import datetime
from value_sort import days
from config import invalid_link_to_post


def formating_noted(txt:str):
    if txt in invalid_link_to_post:
        return 'Нет'
    else:
        formating_txt = txt.replace('\n', ' ')
        return formating_txt


def date_formating(txt:str)-> str:
    """
    Преобразовывает доту из YY.MM.DD в YY-MM-DD
    :param txt:
    :return:
    """
    if txt not in invalid_link_to_post:
        date_list = txt.replace('\n', ' ').replace(',', '.').split('.')
        date_datetime = date_list[2] + '-' + date_list[1] + '-' + date_list[0]
        return date_datetime
    else:
        return ''

def from_watch_in_hours(element:str):
    """
    Функция принимает переменную (XX.XX-XX.XX) типа str, обрабатываем значение(меняем . на :, меняем , на .), 
    разделяет методом split по знаку "-", (XX:XX,XX:XX), получаем сумму минут от преого и второго значнеие, 
    находм разницу и взовращаем это значение
    """
    if element == '':
        return 0
    else:
        formating_element = (element.replace(' ', '').replace('.', ':').replace(',', '.')).replace('—','-').replace('–','-').replace("−",'-')
        formating_elements = formating_element.split('-')
        firts_time =  formating_elements[0].find(':')
        second_time =  formating_elements[1].find(':')
        start_time =  int(formating_elements[0][:firts_time]) * 60 + int(formating_elements[0][firts_time+1:])
        finish_time = int(formating_elements[1][:second_time]) * 60 + int(formating_elements[1][second_time+1:])
        summa_hours = finish_time - start_time
        resault = summa_hours / 60
        return resault

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
                    'Note':formating_noted(row[9]),
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
    if work_day['Data'] not in invalid_link_to_post:
        date_json = work_day['Data']
        data_sort = datetime.datetime.strptime(date_json, '%Y-%m-%d').date()
        if data_sort == days(argument, day=day_read):
            description_for_show_work_day = (f"🎓 Программа: {work_day['Programm']} \n📗Предмет: {work_day['Item']}\n👨‍🏫Преподаватель: {work_day['Teacher']}\n🗓Дата: "
                           f"{work_day['Data']}\n🕐Время: {work_day['Trowme']}\n❗Примичание: {work_day['Note']}\n📌Оператор: {work_day['Operator']}\n🔒Акаунт: {work_day['Account']}.")
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
    print(work_day['Data'])
    if work_day['Data'] not in invalid_link_to_post:
        date_json = work_day['Data']
        data_sort = datetime.datetime.strptime(date_json, '%Y-%m-%d').date()
        if data_sort in date_base_day:
            description = (f"🎓Программа: {work_day['Programm']} \n📗Предмет: {work_day['Item']}\n👨‍🏫Преподаватель: {work_day['Teacher']}\n🗓Дата: "
                           f"{work_day['Data']}\n🕐Время: {work_day['Trowme']} \n❗Примичание: {work_day['Note']} \n📌Оператор: {work_day['Operator']}\n🔒Акаунт: {work_day['Account']}.")
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
            if work_day['Link to post'] not in invalid_link_to_post:
                hours = work_day['Hours']
                print_hours_day = f'🗓 {work_day["Data"]}    🕰 {str(work_day["Hours"])}\n'
                return hours, print_hours_day
            else:
                pass

