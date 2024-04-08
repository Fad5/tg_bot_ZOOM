import asyncio

from aiogram import Bot, Dispatcher, types, executor, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import datetime
import os

from keybords_for_bot import get_kb_list_db, get_kb_start
from notification import users_is_notifications, hours_correct
from sort_work_day import create_cvs_file
from config import answer_block, TEXT_HOLIDAY, list_info
from accounts import TOKEN, ACCOUNTS_ZOOM, ACCOUNTS_WEBINAR
from parsing import get_info_work_day, read_js, read_js_day, read_js_hours
from value_sort import get_password_mail, list_work_day, check_hours_month

# Функции для работы с бд
from def_for_work_date_base import (is_user, show_db, del_user_db, add_user_db,
                                    update_user_db, get_user_name, show_table)

storge = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storge)

# Функция, которая забирает с сайта файл сортирует и сохраняет в csv файл
create_cvs_file()

# Клавиатура
kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb.add('Аккаунты zoom', 'Операторы Webinar.ru')


class StatesdataBase(StatesGroup):
    dataBase = State()


class StatesReplaceSelf(StatesGroup):
    name = State()


@dp.message_handler(commands='data')
async def cmd_create(message: types.Message) -> None:
    """
    Функция отправляет список из LAST, NEXT и CURRENT недель для проверки
    """
    list_week = list_work_day()
    result = 'LAST WEEK: ' + str(list_week[0]) + '\n' + 'CURRENT WEEK: ' + str(
        list_week[1]) + '\n' + 'NEXT WEEK: ' + str(list_week[2])
    await bot.send_message(message.from_user.id, text=result)


# /db_show - вызывает машину состояний
@dp.message_handler(commands='db_show')
async def name_database(message: types.Message) -> None:
    await message.answer("Напиши имя базы данных!",
                         reply_markup=get_kb_list_db())

    await StatesdataBase.dataBase.set()


@dp.message_handler(filters.Text(contains=['отмена', 'Отмена'], ignore_case=True), state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    """
    Функция прерывает машину состояний 
    """
    await state.finish()
    await message.reply('Вы прервали действие', reply_markup=get_kb_start())


@dp.message_handler(filters.Text(contains=['Показать список DataBase',
                                           'показать список database'], ignore_case=True), state='*')
async def cmd_show_table(message: types.Message):
    result = str(show_table())
    await bot.send_message(message.from_user.id, text=result)


@dp.message_handler(state=StatesdataBase.dataBase)
async def load_description(message: types.Message, state: FSMContext) -> None:
    """

    """
    async with state.proxy() as database:
        database['dataBase'] = message.text
    date_base = show_db(table=database['dataBase'].lower())
    await bot.send_message(message.from_user.id, text=str(date_base), parse_mode='HTML')
    await state.finish()


@dp.message_handler(commands='list_db')
async def list_db(massage: types.Message) -> None:
    result = str(show_table())
    await bot.send_message(massage.from_user.id, text=result)


@dp.message_handler(filters.Text(contains='Последнее обновление'))
async def update_user(massage: types.Message) -> None:
    """
    Функция читает report_parsing.txt и отправляет последние значение,
    последнее обновление файла data_base.csv
    """
    date_update_file_unix = os.path.getmtime('data_base.csv')
    date_update_file = str(datetime.datetime.fromtimestamp(date_update_file_unix))
    info_data_update = date_update_file[:-7]
    await bot.send_message(massage.from_user.id, text=info_data_update)


@dp.message_handler(commands='last_upd')
async def upd_user(message: types.Message) -> None:
    date_update_file_unix = os.path.getmtime('data_base.csv')
    date_update_file = str(datetime.datetime.fromtimestamp(date_update_file_unix))
    info_data_update = date_update_file[:-7]
    await bot.send_message(message.from_user.id, text=info_data_update)


@dp.message_handler(commands='upd')
async def upd_user(message: types.Message) -> None:
    await message.answer("Введите имя как в Excel!",
                         reply_markup=get_kb_list_db())
    await StatesReplaceSelf.name.set()


@dp.message_handler(state=StatesReplaceSelf.name)
async def update_user_states(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as name:
        name['dataBase'] = message.text
        update_user_db('user_name', name['dataBase'].replace('==', ' '), 429845350, 'user')
        await bot.send_message(message.from_user.id, text='Ок', reply_markup=get_kb_start())
        await state.finish()


@dp.message_handler(commands='update_user_db')
async def update_user_tg(massage: types.Message) -> None:
    """
    Функция получает сообщение разделяет на 4 части, 1 - команда, 2 - id_tg или user_name, 3 - новое значение, 4 - id_tg
    обновляет данные
    :param massage:
    :return: None
    """
    is_id = is_user(massage.from_user.id, 'admin')
    if is_id:
        message = massage.text
        message_split = message.split()
        if len(message_split) == 2:
            if message_split[1].lower() == 'info':
                await bot.send_message(massage.from_user.id,
                                       text='Пример: /add_user_db id_tg user_name \nПервый аргумент: id или name_user,'
                                            '\n Второй аргумент(новое значение): new name\n'
                                            'Третий аргумент: id_tg Четвертый аргумент: datebase\n'
                                            'Для просмотра баз данных введите команду /list_db')
        elif len(message_split) == 5:
            value = message_split[1]
            name_user = message_split[2].replace('==', ' ')
            id_tg = int(message_split[3])
            database = message_split[4]
            update_user_db(value, name_user, id_tg, database)
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
    result = is_user(id_tg=massage.from_user.id, table='admin')
    if result:
        user_id = massage.text.split()
        if len(user_id) == 2:
            if user_id[1].lower() == 'info':
                await bot.send_message(massage.from_user.id,
                                       text='Первый аргумент: id_TG \n'
                                            'Второй аргумент: database\n'
                                            'Пример: /check_user 123456 user')
        elif len(user_id) == 3:
            id_int = int(user_id[1])
            database = user_id[2]
            result = is_user(id_tg=id_int, table=database)
            if result:
                await bot.send_message(massage.from_user.id, text='Ок')
            else:
                await bot.send_message(massage.from_user.id, text='❗Нет в базе данных')

        else:
            await bot.send_message(massage.from_user.id, text='❗Введите id и базу данных')

    else:
        await bot.send_message(massage.from_user.id, text='🔒У вас нет доступа')


@dp.message_handler(commands='db_show_')
async def db_show(massage: types.Message) -> None:
    """
    Функция для получения всех данных с базы данных
    :param massage:
    :return:
    """
    is_id = is_user(massage.from_user.id, 'admin')
    if is_id:
        message = massage.text
        message_split = message.split()
        if len(message_split) == 2:
            if message_split[1].lower() == 'info':
                await bot.send_message(massage.from_user.id, text='Пример:/db_show database')
            else:
                date_base = show_db(table=message_split[1].lower())
                await bot.send_message(massage.from_user.id, text=str(date_base), parse_mode='HTML')
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
            await bot.send_message(massage.from_user.id,
                                   text='Введите команду, id, и database к которому подключатся \n Пример:'
                                        '/del_user_db 123456 user')
    elif len(message_split) == 3:
        database = message_split[2]
        id_tg = int(message_split[1])
        result = is_user(id_tg, database)
        if result:
            del_user_db(id_tg, database)
            await bot.send_message(massage.from_user.id, text='❗Пользователь с таким id удален из базы данных!')
        else:
            await bot.send_message(massage.from_user.id, text='❗Пользователь с таким id не найден!')
    else:
        await bot.send_message(massage.from_user.id, text='❗Введите команду, id и database')


@dp.message_handler(commands='admin_commands')
async def check_user_tg(massage: types.Message):
    """
    Отправляет все возможные команды для администраторов
    """
    result = is_user(id_tg=massage.from_user.id, table='admin')
    if result:
        await bot.send_message(massage.from_user.id, text='/add_user_db - добавить пользователя \n'
                                                          '/del_user_db - удалить пользователя \n'
                                                          '/db_show - показать базу данных \n'
                                                          '/check_user - проверка в базе данных\n'
                                                          '/list_db - список database')
    else:
        await bot.send_message(massage.from_user.id, text='🔒У вас нет доступа')


@dp.message_handler(commands='add_user_db')
async def add_user(massage: types.Message) -> None:
    """
    Функция, которая добавляет пользователя в базу данных, fun получает текст сообщения и split [1]-id, [2] - name_user
    если написать в боте команду и info, бот отправит пример для выполнения этой функции
    :param massage:
    :return: None
    """
    is_id = is_user(massage.from_user.id)
    if is_id:
        message = massage.text
        message_split = message.split()
        if len(message_split) == 2:
            if message_split[1].lower() == 'info':
                await bot.send_message(massage.from_user.id,
                                       text='Введите команду, id, и database к которому подключатся \n Пример: '
                                            '/add_user_db 123456 Имя==Фамилия в exel user')
        elif len(message_split) == 4:
            id_tg = int(message_split[1])
            name_user = message_split[2].replace('==', ' ')
            database = message_split[3]
            result = add_user_db(id_tg, name_user, database)
            if result:
                await bot.send_message(massage.from_user.id, text='Ок')
            else:
                await bot.send_message(massage.from_user.id, text='Пользователь c таким id существует ')
        else:
            await bot.send_message(massage.from_user.id, text='❗Введите команду ,id и database')
    else:
        await bot.send_message(massage.from_user.id, text='🔒У вас нет доступа')


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


# /start - функция запуска бота
@dp.message_handler(commands='start')
async def start_handler(massage: types.Message):
    result = get_user_name(massage.from_user.id, 'user')
    if result is not None:
        await massage.answer(f'👋 Привет,{massage.from_user.first_name}!', reply_markup=get_kb_start())
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


# /next_week - функция сначала смотри есть ли вы в базе данных, а потом проходится 
# по data_base.csv файлу и возвращают все zoom
@dp.message_handler(commands='next_week')
async def get_next_week_work(massage: types.Message):
    result = get_user_name(massage.from_user.id, 'user')
    if result is not None:
        for i in (get_info_work_day(result)):
            info = read_js_day(i, list_work_day()[2])
            if info is not None:
                list_info.append(info)
                await massage.answer(info)
        if not list_info:
            await bot.send_message(massage.from_user.id, text=TEXT_HOLIDAY)

        list_info.clear()
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


# /current_week - функция сначала смотрит есть ли вы в базе данных, а потом проходится 
# по data_base.csv файлу и возвращают все zoom
@dp.message_handler(commands='current_week')
async def get_current_week_work(massage: types.Message):
    result = get_user_name(massage.from_user.id, 'user')
    if result is not None:
        for i in (get_info_work_day(result)):
            info = read_js_day(i, list_work_day()[1])
            if info is not None:
                list_info.append(info)
                await massage.answer(info)
        if not list_info:
            await bot.send_message(massage.from_user.id, text=TEXT_HOLIDAY)
        list_info.clear()
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


# /last_week - функция сначала смотрит есть ли вы в базе данных, а потом проходится 
# по data_base.csv файлу и возвращают все zoom
@dp.message_handler(commands='last_week')
async def get_last_week_work(massage: types.Message):
    result = get_user_name(massage.from_user.id, 'user')
    if result is not None:
        for i in (get_info_work_day(result)):
            info = read_js_day(i, list_work_day()[0])
            if info is not None:
                list_info.append(info)
                await massage.answer(info)
        if not list_info:
            await bot.send_message(massage.from_user.id, text=TEXT_HOLIDAY)
        list_info.clear()
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


# /today - функция сначала смотрит есть ли вы в базе данных, а потом проходится
# по data_base.csv файлу и возвращают все zoom в этот день
@dp.message_handler(commands='today')
async def get_today_work_day(massage: types.Message):
    """
    Получает трансляций на сегодня
    :param massage:
    :return:
    """
    result = get_user_name(massage.from_user.id, 'user')
    if result is not None:
        for i in (get_info_work_day(result)):
            info = read_js(work_day=i, argument='')
            if info is not None:
                list_info.append(info)
                await massage.answer(info)
        if not list_info:
            await bot.send_message(massage.from_user.id, text=TEXT_HOLIDAY)
        list_info.clear()
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


# /tomorrow - функция сначала смотрит есть ли вы в базе данных, а потом проходится 
# по data_base.csv файлу и возвращают все zoom в этот день
@dp.message_handler(commands='tomorrow')
async def get_tomorrow_work_day(massage: types.Message) -> None:
    """
    Получает трансляций на завтра
    :param massage:
    :return:
    """
    result = get_user_name(massage.from_user.id, 'user')
    if result is not None:
        for i in (get_info_work_day(result)):
            info = read_js(work_day=i, argument='next')
            if info is not None:
                list_info.append(info)
                await massage.answer(info)
        if not list_info:
            await bot.send_message(massage.from_user.id, text=TEXT_HOLIDAY)
        list_info.clear()
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


# /yesterday - функция сначала смотрит есть ли вы в базе данных, а потом проходится 
# по data_base.csv файлу и возвращают все zoom в этот день
@dp.message_handler(commands='yesterday')
async def get_yesterday_work_day(massage: types.Message) -> None:
    """ 
    Функция для получения трансляций на вчерашний день
    :param massage:
    :return:
    """
    result = get_user_name(massage.from_user.id, 'user')
    if result is not None:
        for i in (get_info_work_day(result)):
            info = read_js(work_day=i, argument='last')
            if info is not None:
                list_info.append(info)
                await massage.answer(info)
        if not list_info:
            await bot.send_message(massage.from_user.id, text=TEXT_HOLIDAY)
        list_info.clear()
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


# /get_summa_hours_current_month - функция сначала смотрит есть ли вы в базе данных, а потом проходится 
# по data_base.csv файлу и возвращает сумму часов в текущем месяце
@dp.message_handler(commands=f'get_summa_hours_current_month')
async def get_hours_summa_current(massage: types.Message, summa: float = 0) -> None:
    result = get_user_name(massage.from_user.id, 'user')
    if result is not None:
        date_list = check_hours_month('current_list_hours')
        for i in (get_info_work_day(result)):
            hours = read_js_hours(i, date_list)
            print(hours)
            if hours is None:
                pass
            else:
                summa = summa + float(hours[0])
        await bot.send_message(massage.from_user.id, text='🕰 ' + str("%.2f" % summa))
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


# /get_list_hours_current_month - функция сначала смотрит есть ли вы в базе данных, а потом проходится 
# по data_base.csv файлу и возвращает список часов в текущем месяце
@dp.message_handler(commands=f'get_list_hours_current_month')
async def get_hours_list_current(massage: types.Message, print_hours: str = '') -> None:
    result = get_user_name(massage.from_user.id, 'user')
    if result is not None:
        date_list = check_hours_month('current_list_hours')
        for i in (get_info_work_day(result)):
            hours = read_js_hours(i, date_list)
            if hours is None:
                pass
            else:
                print_hours = print_hours + hours[1]
        await bot.send_message(massage.from_user.id, text=print_hours)
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


# /get_summa_hours_last_month - функция сначала смотрит есть ли вы в базе данных, а потом проходится 
# по data_base.csv файлу и возвращает сумму часов в прошлом месяце
@dp.message_handler(commands=f'get_summa_hours_last_month')
async def get_hours_summa_last(massage: types.Message, summa: float = 0, print_hours: str = '') -> None:
    result = get_user_name(massage.from_user.id, 'user')
    if result is not None:
        date_list = check_hours_month('last_list_hours')
        for i in (get_info_work_day(result)):
            hours = read_js_hours(i, date_list)
            if hours is None:
                pass
            else:
                summa = summa + float(hours[0])
        await bot.send_message(massage.from_user.id, text='🕰 ' + str("%.2f" % summa))
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


# /get_list_hours_last_month - функция сначала смотрит есть ли вы в базе данных, а потом проходится 
# по data_base.csv файлу и возвращает список часов в прошлом месяце
@dp.message_handler(commands=f'get_list_hours_last_month')
async def get_hours_list_last(massage: types.Message, print_hours: str = '') -> None:
    result = get_user_name(massage.from_user.id, 'user')
    if result is not None:
        date_list = check_hours_month('last_list_hours')
        for i in (get_info_work_day(result)):
            hours = read_js_hours(i, date_list)
            if hours is None:
                pass
            else:
                print_hours = print_hours + hours[1]
        await bot.send_message(massage.from_user.id, text=print_hours)
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


# Создание кнопок, которые берется из ACCOUNTS_ZOOM и ACCOUNTS_WEBINAR,
# Кнопки будут состоять из названий аккаунтов
@dp.message_handler()
async def get_info_accounts(massage: types.Message):
    result = get_user_name(massage.from_user.id, 'user')
    if result is not None:
        if massage.text.lower() == 'аккаунты zoom':
            await bot.send_message(massage.from_user.id, '<b>Аккаунты ZOOM</b>', parse_mode='HTML',
                                   reply_markup=get_keyboard('ZOOM', ACCOUNTS_ZOOM))
        elif massage.text.lower() == 'операторы webinar.ru':
            await bot.send_message(massage.from_user.id, '<b>Операторы Webinar.ru</b>', parse_mode='HTML',
                                   reply_markup=get_keyboard('webinar', ACCOUNTS_WEBINAR))
    else:
        await bot.send_message(massage.from_user.id, text=answer_block)


# Это функция срабатывает при нажатии на кнопку и возражает информацию об аккаунте
@dp.callback_query_handler(text_contains='ZOOM')
async def show_password_mail_zoom(callback_query: types.CallbackQuery):
    button_name = callback_query['data'].replace('ZOOM', '')
    date = get_password_mail(button_name, ACCOUNTS_ZOOM)
    await bot.send_message(callback_query.from_user.id, parse_mode='html', text=date)
    await callback_query.answer()


# Это функция срабатывает при нажатии на кнопку и возражает информацию об аккаунте
@dp.callback_query_handler(text_contains='webinar')
async def show_password_mail_webinar(callback_query: types.CallbackQuery):
    button_name = callback_query['data'].replace('webinar', '')
    date = get_password_mail(button_name, ACCOUNTS_WEBINAR)
    await bot.send_message(callback_query.from_user.id, parse_mode='html', text=date)
    await callback_query.answer()


# Эхо функция
@dp.message_handler()
async def echo(massage: types.Message):
    await bot.send_message(massage.from_user.id, massage.text)


chat_ids = {'429845350'}


async def notification(sleep_for):
    while True:
        await asyncio.sleep(sleep_for)
        for i in users_is_notifications:
            user_name = i[1]
            user_id = i[0]
            data = get_info_work_day(user_name)
            is_zoom = hours_correct(data)
            if is_zoom:
                await bot.send_message(user_id, f'{user_name} запусти zoom через час', disable_notification=True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(notification(60))
    executor.start_polling(dp, skip_updates=True)
