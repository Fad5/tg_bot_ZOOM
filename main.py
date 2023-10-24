import datetime

from aiogram import Bot, Dispatcher, types, executor
from config import answer_block, TEXT_HOLIDAY, list_info
from accounts import TOKEN, ACCOUNTS_ZOOM,ACCOUNTS_WEBINAR
from parsing import get_info_work_day, read_js, read_js_day, read_js_hours
from sort_work_day import create_cvs_file
from value_sort import get_password_mail, list_work_day, check_hours_month
import threading
# Функции для работы с бд
from def_for_work_date_base import is_user, show_db, del_user_db, add_user_db, update_user_db, get_user_name, show_table

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Функиция которая забирает с сайта файл  сортирует и сохранияет в csv файл
create_cvs_file()

kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb.add('Аккаунты zoom', 'Операторы Webinar.ru')


# Команды для админа

@dp.message_handler(commands='list_db')
async def list_db(massage: types.Message) -> None:

        result = show_table()
        await bot.send_message(massage.from_user.id, text=result)


@dp.message_handler(commands='update_user_db')
async def update_user(massage: types.Message) -> None:
    """
    Фунцкия получает сообщение разделяет на 4 части, 1 - команда, 2 - id_tg или user_name, 3 - новое значение, 4 - id_tg
    обнавляет данные
    :param massage:
    :return: None
    """
    is_id = is_user(massage.from_user.id,'admin')
    if is_id == True:
        message = massage.text
        message_split = message.split()
        print(message_split)
        if len(message_split) == 2:
            if message_split[1].lower() == 'info':
                await bot.send_message(massage.from_user.id,
                                       text='Пример: /add_user_db id_tg user_name \nПервый аргумент: id или name_user,'
                                            '\n Второй аргумент(новое значение): new name\n'
                                            'Третий аргумент: id_tg Четвертый аргумен: datebase\n'
                                            'Для просмотра баз данных введите команду /list_db')
        elif len(message_split) == 5:    
            value = message_split[1]
            name_user = message_split[2].replace('__',' ')
            id_tg = int(message_split[3])
            datebase = message_split[4]
            update_user_db(value, name_user, id_tg,datebase)
            await bot.send_message(massage.from_user.id, text='Ок')
        else:
            await bot.send_message(massage.from_user.id, text='Введите команду и id')
    else:
        await bot.send_message(massage.from_user.id, text='🔒У вас нет доступа')


@dp.message_handler(commands='check_user')
async def check_user(massage: types.Message) -> None:
    """
    Проверка в базе данных через id
    :param massage:
    :return:
    """
    result = is_user(id_tg=massage.from_user.id, database='admin')
    if result == True:
        user_id = massage.text.split()
        if len(user_id) == 2:
            if user_id[1].lower() == 'info':
                    await bot.send_message(massage.from_user.id,
                                           text='Первый аргумент: id_TG \n'
                                            'Второй аргумент: datebase\n'
                                            'Пример: /check_user 123456 user')
        elif len(user_id) == 3:
            id_int = int(user_id[1])
            datebase = user_id[2]
            result = is_user(id_tg=id_int,database=datebase)
            if result == True:
                await bot.send_message(massage.from_user.id, text='Ок')
            else:
                await bot.send_message(massage.from_user.id, text='❗Нет в базе данных')

        else:
            await bot.send_message(massage.from_user.id, text='❗Введите id и базу данных')

    else:
        await bot.send_message(massage.from_user.id, text='🔒У вас нет доступа')


@dp.message_handler(commands='db_show')
async def db_show(massage: types.Message) -> None:
    """
    Функция для получения всех данных с базы данных
    :param massage:
    :return:
    """
    is_id = is_user(massage.from_user.id,'admin')
    if is_id == True:
        message = massage.text
        message_split = message.split()
        if len(message_split) == 2:
            if message_split[1].lower() == 'info':
                await bot.send_message(massage.from_user.id, text='Пример:/db_show datebase')
            else:
                    date_base = show_db(database=message_split[1].lower())
                    await bot.send_message(massage.from_user.id, text=str(date_base),parse_mode='HTML')
    else:
        await bot.send_message(massage.from_user.id, text='🔒У вас нет доступа')


@dp.message_handler(commands='del_user_db')
async def del_user(massage: types.Message) -> None:
    """
    Функция для получения всех данных с базы данных
    :param massage:
    :return:
    """
    message_split = massage.text.split()
    if len(message_split) == 2:
        if message_split[1].lower() == 'info':
            await bot.send_message(massage.from_user.id, text='Введите команду, id, и datebase к которому подключатся \n Пример:'
                         '/del_user_db 123456 user')
    elif len(message_split) == 3:
        datebase =  message_split[2]
        id_tg = int(message_split[1])
        result = is_user(id_tg,datebase)
        if result == True:
            del_user_db(id_tg,datebase)
            await bot.send_message(massage.from_user.id, text='❗Пользователь с таким id удален из базы данных!')
        else:
            await bot.send_message(massage.from_user.id, text='❗Пользователь с таким id не найден!')
    else:
        await bot.send_message(massage.from_user.id, text='❗Введите команду, id и datebase')


@dp.message_handler(commands='admin_commands')
async def check_user(massage: types.Message):
    result = is_user(id_tg=massage.from_user.id, database='admin')
    if result == True:
        await bot.send_message(massage.from_user.id, text='/add_user_db - добавить пользователя \n'
                                                      '/del_user_db - удалить пользователя \n'
                                                      '/db_show - показать базу данных \n'
                                                      '/check_user - проверка в базе данных\n'
                                                      '/list_db - список datebase')
    else:
        await bot.send_message(massage.from_user.id, text='🔒У вас нет доступа')


@dp.message_handler(commands='add_user_db')
async def add_user(massage: types.Message) -> None:
    """
    Функция которая добавляет пользователя в базу данных, fun получает текст сообщения и split [1]-id, [2] - name_user
    если написать в бота команду и info, бот отправит пример для выполнения этой функции
    :param massage:
    :return: None
    """
    is_id = is_user(massage.from_user.id)
    if is_id == True:
        message = massage.text
        message_split = message.split()
        if len(message_split) == 2:
            if message_split[1].lower() == 'info':
                await bot.send_message(massage.from_user.id,
                                      text='Введите команду, id, и datebase к которому подключатся \n Пример: '
                                      '/add_user_db 123456 Имя__Фамилия в exel user')
        elif len(message_split) == 4:
            id_tg = int(message_split[1])
            name_user = message_split[2].replace('__',' ')
            datebase = message_split[3]
            result = add_user_db(id_tg, name_user,datebase)
            if result == True:
                await bot.send_message(massage.from_user.id, text='Ок')
            else:
                await bot.send_message(massage.from_user.id, text='Пользователь c таким id существует ')
        else:
            await bot.send_message(massage.from_user.id, text='❗Введите команду ,id и datebase')
    else:
        await bot.send_message(massage.from_user.id, text='🔒У вас нет доступа')


# Команды для пользователей
# Меню с аккаунтами zoom
def get_keyboard(name_callback, ACCOUNTS):
    callback_data_zoom = []
    for account in ACCOUNTS:
        element = name_callback + account
        callback_data_zoom.append(element)
    keyboard = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton(text='', callback_data="MainMenu")
    button_list = [types.InlineKeyboardButton(text=x.replace(name_callback, ''), callback_data=x) for x in
                   callback_data_zoom]
    keyboard.add(*button_list, back_button)
    return keyboard


@dp.message_handler(commands='start')
async def start_handler(massage: types.Message):
    print(massage.from_user.id)
    result = get_user_name(massage.from_user.id, 'user')
    if result != None:
        await massage.answer(f'👋 Привет,{massage.from_user.first_name}!', reply_markup=kb)
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


@dp.message_handler(commands='next_week')
async def get_next_week_work(massage: types.Message):
    result = get_user_name(massage.from_user.id, 'user')
    if result != None:
        for i in (get_info_work_day(result)):
            info = read_js_day(i, list_work_day()[2])
            if info != None:
                list_info.append(info)
                await massage.answer(info)
        if list_info == []:
            await bot.send_message(massage.from_user.id, text=TEXT_HOLIDAY)

        list_info.clear()
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


@dp.message_handler(commands='current_week')
async def get_current_week_work(massage: types.Message):
    result = get_user_name(massage.from_user.id, 'user')
    if result != None:
        for i in (get_info_work_day(result)):
            info = read_js_day(i, list_work_day()[1])
            if info != None:
                list_info.append(info)
                await massage.answer(info)
        if list_info == []:
            await bot.send_message(massage.from_user.id, text=TEXT_HOLIDAY)
        list_info.clear()
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


@dp.message_handler(commands='last_week')
async def get_last_week_work(massage: types.Message):
    result = get_user_name(massage.from_user.id, 'user')
    if result != None:
        for i in (get_info_work_day(result)):
            info = read_js_day(i,list_work_day()[0])
            if info != None:
                list_info.append(info)
                await massage.answer(info)
        if list_info == []:
            await bot.send_message(massage.from_user.id, text=TEXT_HOLIDAY)
        list_info.clear()
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


@dp.message_handler(commands='today')
async def get_today_work_day(massage: types.Message):
    result = get_user_name(massage.from_user.id, 'user')
    if result != None:
        for i in (get_info_work_day(result)):
            info = read_js(work_day=i, argument='')
            if info != None:
                list_info.append(info)
                await massage.answer(info)
        if list_info == []:
            await bot.send_message(massage.from_user.id, text=TEXT_HOLIDAY)
        list_info.clear()
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


@dp.message_handler(commands='tomorrow')
async def get_tomorrow_work_day(massage: types.Message) -> None:
    """
    Полученеи трансляций на завтра
    :param massage:
    :return:
    """
    result = get_user_name(massage.from_user.id, 'user')
    if result != None:
        for i in (get_info_work_day(result)):
            info = read_js(work_day=i, argument='next')
            if info != None:
                list_info.append(info)
                await massage.answer(info)
        if list_info == []:
            await bot.send_message(massage.from_user.id, text=TEXT_HOLIDAY)
        list_info.clear()
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


@dp.message_handler(commands='yesterday')
async def get_yesterday_work_day(massage: types.Message) -> None:
    """ 
    Полученеи трансляций на вчерашний день
    :param massage:
    :return:
    """
    result = get_user_name(massage.from_user.id, 'user')
    if result != None:
        for i in (get_info_work_day(result)):
            info = read_js(work_day=i, argument='last')
            if info != None:
                list_info.append(info)
                await massage.answer(info)
        if list_info == []:
            await bot.send_message(massage.from_user.id, text=TEXT_HOLIDAY)
        list_info.clear()
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


@dp.message_handler(commands=f'get_summa_hours_current_month')
async def get_hours_summa_current(massage: types.Message, summa: int = 0, print_hours: str = '') -> None:
    result = get_user_name(massage.from_user.id, 'user')
    if result != None:
        for i in (get_info_work_day(result)):
            hours = read_js_hours(i, check_hours_month('current_list_hours'))
            if hours == None:
                pass
            else:
                summa = summa + hours[0]
                print_hours = print_hours + hours[1]
        await bot.send_message(massage.from_user.id, text='🕰 '+str(summa))
    else:
       await bot.send_message(massage.from_user.id, text=answer_block)


@dp.message_handler(commands=f'get_list_hours_current_month')
async def get_hours_list_current(massage: types.Message, summa: int = 0, print_hours: str = '') -> None:
    result = get_user_name(massage.from_user.id, 'user')
    if result != None:
        for i in (get_info_work_day(result)):
            hours = read_js_hours(i, check_hours_month('current_list_hours'))
            if hours == None:
                pass
            else:
                summa = summa + hours[0]
                print_hours = print_hours + hours[1]
        await bot.send_message(massage.from_user.id, text=print_hours)
    else:
       await bot.send_message(massage.from_user.id, text=answer_block)


@dp.message_handler(commands=f'get_summa_hours_last_month')
async def get_hours_summa_last(massage: types.Message, summa: int = 0, print_hours: str = '') -> None:
    result = get_user_name(massage.from_user.id, 'user')
    if result != None:
        for i in (get_info_work_day(result)):
            hours = read_js_hours(i, check_hours_month('last_list_hours'))
            if hours == None:
                pass
            else:
                summa = summa + hours[0]
                print_hours = print_hours + hours[1]
        await bot.send_message(massage.from_user.id, text='🕰 '+str(summa))
    else:
       await bot.send_message(massage.from_user.id, text=answer_block)


@dp.message_handler(commands=f'get_list_hours_last_month')
async def get_hours_list_last(massage: types.Message, summa: int = 0, print_hours: str = '') -> None:
    result = get_user_name(massage.from_user.id, 'user')
    if result != None:
        for i in (get_info_work_day(result)):
            hours = read_js_hours(i, check_hours_month('last_list_hours'))
            if hours == None:
                pass
            else:
                summa = summa + hours[0]
                print_hours = print_hours + hours[1]
        await bot.send_message(massage.from_user.id, text=print_hours)
    else:
       await bot.send_message(massage.from_user.id, text=answer_block)


@dp.message_handler()
async def get_info_accounts(massage: types.Message):
    result = get_user_name(massage.from_user.id, 'user')
    if result != None:
        if massage.text.lower() == 'аккаунты zoom':
            await bot.send_message(massage.from_user.id, '<b>Аккаунты ZOOM</b>', parse_mode='HTML',
                                   reply_markup=get_keyboard('ZOOM', ACCOUNTS_ZOOM))
        elif massage.text.lower() == 'операторы webinar.ru':
            await bot.send_message(massage.from_user.id, '<b>Операторы Webinar.ru</b>', parse_mode='HTML',
                                   reply_markup=get_keyboard('webinar', ACCOUNTS_WEBINAR))
    else:
       await bot.send_message(massage.from_user.id, text=answer_block)


@dp.callback_query_handler(text_contains='ZOOM')
async def show_password_mail(callback_query: types.CallbackQuery):
    button_name = callback_query['data'].replace('ZOOM', '')
    date = get_password_mail(button_name, ACCOUNTS_ZOOM)
    await bot.send_message(callback_query.from_user.id, parse_mode='html', text=date)
    await callback_query.answer()


@dp.callback_query_handler(text_contains='webinar')
async def show_password_mail(callback_query: types.CallbackQuery):
    button_name = callback_query['data'].replace('webinar', '')
    date = get_password_mail(button_name, ACCOUNTS_WEBINAR)
    await bot.send_message(callback_query.from_user.id, parse_mode='html', text=date)
    await callback_query.answer()


@dp.message_handler()
async def echo(massage: types.Message):
    await bot.send_message(massage.from_user.id, massage.text)

def start():
    executor.start_polling(dp, skip_updates=True)
    threading.Timer(86400, start).start()
    

if __name__ == '__main__':
    start()