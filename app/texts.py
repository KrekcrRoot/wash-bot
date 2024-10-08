action_canceled = 'Действие отменено, напишите "/start" для начала работы'
help = 'help'

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
machine_changing_title = 'Напишите новое имя машинки:'
machine_title_changed = 'Имя машинки успешно изменено'

#Status
status_free = 'Стиралка не занята'

def status_broken(reason):
    return f"Стирка сейчас не доступна, причина:\n{reason}"

def status_busy(tag, time):
    return f"Стиралка занята\nЕе использует: {tag}\nВремя начала использования: {time}"

def status_ordered(washer_tag, time, waiter_tag):
    return f"Стиралка занята\n\nЕе использует: {washer_tag}\nВремя начала использования: {time}\nЗа ним еще в очереди стоит чел: {waiter_tag}"

def status_waiting(tag,time):
    return f"Стиралка закончила стирку, но чел который был в очереди еще не закинул вещи\nВот он: {tag}\nВремя начала использования: {time}"

#Wash
wash_executes = 'Стирка идет'
wash_executes_queue = 'Стирка идет, вы в очереди'
wash_queue = 'Стирка закончилась, ваша очередь'

#Admin
admin_add_user = 'Укажите пользователя в следующем формате: [tag] [room]\n\nНапример:\n@Ivan 1101/3'
admin_user_added = 'Пользователь был успешно добавлен'
admin_kick_user = 'Выберите какого пользователя вы хотите исключить из списка ниже:'
admin_user_kicked = 'Пользователь был успешно исключен'
admin_machine_fixed = 'Стирка вновь доступна для данной машинки '
admin_machine_stopped = 'Стирка запрещена, люди уведомлены о причине'
admin_stopping_machine = 'Укажите причину:'
admin_transfering_rights = 'Укажите пользователя в следующем формате: [tag]\n\nНапример:\n@Ivan'
admin_rights_transfered = 'Права администратора успешно переданы, напишите "/start" чтобы продолжить'

def admin_machine(title):
    return f'Вы сейчас администрируете стиралку: {title}'

#Reports
report_broke = 'Машинка сломана'
report_select = 'Выберите проблему из списка:'
report_forgotten_photo = 'Пришлите фото забытых вещей:'
report_forgotten_noticed = 'Люди были уведомлены'
report_broke_noticed = 'Люди были уведомлены'

#Confirmations
confirm_occupy = 'Вы уверены?'
confirm_break = 'Вы уверены?'

#Errors
error_getting_user = 'Что-то пошло не так при получении информации о пользователе'
error_getting_status = 'Что-то пошло не так при получении статуса'
error_getting_order = 'Что-то пошло не так при получении инфформации об очереди'
error_getting_machines = 'Что-то пошло не так при получении информации о списке стиралок'
error_checking_admin = 'Что-то пошло не так при проверка на админа'
error_user_not_admin = 'Вы не админ'
error_admin_add_user = 'Не получилось добавить пользователя, что-то пошло не так'
error_admin_kick_user = 'Не получилось исключить пользователя, что-то пошло не так'
error_admin_kick_user_list = 'Не получилось получить список пользователей, что-то пошло не так'
error_admin_kick_user_none = "К данной машинке никто не привязан"
error_admin_user_wrong_format = 'Неверный формат записи'
error_stopping_machine = 'Не получилось запретить стирку, что-то пошло не так'
error_stopping_machine_format = 'Неверно указана причина'
error_transfering_rights = 'Не получилось передать права администратора, что-то пошло не так'
error_transfering_rights_format = 'Неверно указан тег'
error_machine_fix = 'Не получилось разрешить стирку, что-то пошло не так'
error_machine_link = 'Что-то пошло не так при привязке'
error_machine_unlink = 'Что-то пошло не так при отвязке'
error_machine_name = 'Неверно указано название машинки'
error_machine_changing_title = 'Не получилось изменить имя машинки, что-то пошло не так'
error_machine_changing_title_format = 'Неверно указано название машинки'
error_wash_end = 'Не получилось закончить стирку, что-то пошло не так'
error_wash_occupy = 'Не получилось занять машинку, что-то пошло не так'
error_wash_queue = 'Не получилось встать в очередь, что-то пошло не так'
error_order_free = 'Не получилось выйти из очереди, что-то пошло не так'
error_report_broke = 'Что-то пошло не так'

# --- Menu texts ---
def menu_info(user, machines):
    user_machines = ''
    for i in machines:
        user_machines += '\n'+i.title
    
    return f'Тэг: {user.telegram_tag}\nКоличество использований: {user.count}\nОбщее время использования: {user.time}\nВыбранная машинка: {user.link_machine.title}\n\nДоступные машинки:{user_machines}'


menu_help = '❓ Помощь'

menu_yes = '✅ Да'
menu_no = '❌ Нет'
menu_cancel = '🙅‍♂️ Отмена'

menu_status = '📶 Статус'
menu_status_occupy = '🧼 Занять'
menu_status_occupy_from_queue = '🧼 Начать стирку'
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