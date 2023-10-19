from value_sort import name_week_button, list_work_day, check_hours_month



answer_block = '🔒Вас нет в базе данных, обратитесь к @Fad1_1'

TEXT_HOLIDAY = '🛌 У вас выходной'

STREAMING = ['Дни', 'Недели']

# Название кнопок недели
WORK_WEEK = name_week_button()

WORK_WEEK_DAYS = list_work_day()

# Список дней прошлой недели в формате datetime
LAST_WEEK = WORK_WEEK_DAYS[0]

# Список дней текущей недели в формате datetime
CURRENT = WORK_WEEK_DAYS[1]

# Список дней следующей недели в формате datetime
NEXT_WEEK = WORK_WEEK_DAYS[2]

HOURS_CURRENT_MONTH = check_hours_month('current_list_hours')
HOURS_LAST_MONTH = check_hours_month('last_list_hours')

list_info = []