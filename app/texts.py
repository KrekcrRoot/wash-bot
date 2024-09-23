action_canceled = 'Действие отменено, напишите "/start" для начала работы'

def time_elapsed(time):
    return f'Стирка заняла: {time} мин'

#Auth
auth_success = 'Вы успешно авторизованы'
def auth_success_machine(title):
    return auth_success+f'\nВыбранная машинка: {title}'

auth_failed = 'Вы не авторизованы. Обратитесь за помощью к кому скидывались за стиралку'

#Machine
machine_select = 'Выберите стиральную машинку из списка'
machine_no_available = 'У вас нет доступных машин\nНапишите "/start" чтобы продолжить'
machine_only_one = 'Вам доступна только одна машинка, менять не на что'

#Status
status_free = 'Стиралка не занята'

def status_busy(tag, time):
    return f"Стиралка занята\nЕе использует: {tag}\nВремя начала использования: {time}"

def status_ordered(tag, time):
    return f"Стиралка занята\nЕе использует: {tag}\nВремя начала использования: {time}"

def status_waiting(tag,time):
    return f"Стиралка занята\nЕе использует: {tag}\nВремя начала использования: {time}"

#Admin
def admin_machine(title):
    return f'Вы сейчас администрируете стиралку: {title}'

#Reports
report_select = 'Выберите проблему из списка:'
report_forgotten_photo = 'Пришлите фото забытых вещей:'
report_forgotten_noticed = 'Люди были уведомлены'

#Confirmations
confirm_occupy = 'Вы уверены?'
confirm_break = 'Вы уверены?'

#Errors
error_user_not_admin = 'Вы не админ'
error_machine_link = 'Что-то пошло не так при привязке'
error_machine_name = 'Неверно указано название машинки'
error_wash_end = 'Не получилось закончить стирку, что-то пошло не так'

# --- Menu texts ---
menu_help = '❓ Помощь'

menu_yes = '✅ Да'
menu_no = '❌ Нет'
menu_cancel = '🙅‍♂️ Отмена'

menu_status = '📶 Статус'
menu_status_occupy = '🧼 Занять'
menu_status_join_queue = '⏳ Занять очередь'
menu_status_leave_queue = '↩️ Выйти из очереди'
menu_status_end = '🏁 Закончить стирку'

menu_report = '🚨 Сообщить о проблеме'
menu_report_forgotten = '👕 В стиралке забыты вещи'
menu_report_occupied = '🥷🏻 Стиралка занята'
menu_report_break = '🔧 Поломка'

menu_admin = '🛠️ Admin menu'
menu_admin_add_user = 'Добавить пол-я'
menu_admin_kick_user = 'Исключить пол-я'
menu_admin_stop_machine = 'Запретить стирку с указанием причины'
menu_admin_end = 'Принудительно закончить стирку'
menu_admin_fix = 'Разрешить стирку'
menu_admin_change_title = 'Изменить название машинки'
menu_admin_change_admin = 'Передать права администратора'