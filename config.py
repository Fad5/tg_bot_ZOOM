from value_sort import list_work_day

# Правельная ссылка 
invalid_link_to_post = 'http://content.inpsycho.ru/'

# Текст будет отправляетя если человека нет в базе данных
answer_block = '🔒Вас нет в базе данных, обратитесь к @Fad1_1'

# Если нет в эксели записи 
TEXT_HOLIDAY = '🛌 У вас выходной'

# Список в списке в котором назодяться дата дней недели, на эту неделю,
# следующую неделю, прошлую
WORK_WEEK_DAYS = list_work_day()

# Список дней прошлой недели в формате datetime
LAST_WEEK = WORK_WEEK_DAYS[0]

# Список дней текущей недели в формате datetime
CURRENT = WORK_WEEK_DAYS[1]

# Список дней следующей недели в формате datetime
NEXT_WEEK = WORK_WEEK_DAYS[2]

# Переменная сохраняет дни в которые есть работа
list_info: list = []
