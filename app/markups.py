from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

btnStatus = KeyboardButton(text='📶 Статус')

# --- Main Menu ---
btnHelp = KeyboardButton(text='❓ Помощь')
mainMenu = ReplyKeyboardMarkup(keyboard=[[btnStatus, btnHelp]],resize_keyboard=True)

# --- Admin Main Menu ---
btnHelpAdmin = KeyboardButton(text='❓ Помощь')
btnAdminMenu = KeyboardButton(text='🛠️ Admin menu')
mainMenuAdmin = ReplyKeyboardMarkup(keyboard=[[btnStatus, btnAdminMenu, btnHelpAdmin]],resize_keyboard=True)

# -- Report Menu --
btnForgotten = InlineKeyboardButton(text='👕 В стиралке забыты вещи', callback_data='forgotten')
btnOccupied = InlineKeyboardButton(text='🥷🏻 Стиралка занята', callback_data='occupied')
btnBreak = InlineKeyboardButton(text='🔧 Поломка',callback_data='break')
reportMenu = InlineKeyboardMarkup(inline_keyboard=[[btnForgotten],[btnOccupied],[btnBreak]])

# --- Machine selection Menu ---
def machineMenu(machineList):
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=i['title']) for i in machineList]],resize_keyboard=True)

# --- Status Menu ---
btnReport = InlineKeyboardButton(text='🚨 Сообщить о проблеме',callback_data='report')
#occupy menu
btnOccupy = InlineKeyboardButton(text='🧼 Занять',callback_data='occupy')
occupyMenu = InlineKeyboardMarkup(inline_keyboard=[[btnOccupy],[btnReport]])
#queue menu
btnQueue = InlineKeyboardButton(text='⏳ Занять очередь',callback_data='queue')
queueMenu = InlineKeyboardMarkup(inline_keyboard=[[btnQueue]])
#in queue menu
btnFree = InlineKeyboardButton(text='↩️ Выйти из очереди',callback_data='free')
in_queueMenu = InlineKeyboardMarkup(inline_keyboard=[[btnFree]])
#end menu
btnEnd = InlineKeyboardButton(text='🏁 Закончить стирку',callback_data='end')
endMenu = InlineKeyboardMarkup(inline_keyboard=[[btnEnd],[btnReport]])

# --- Forgotten cloth prompt ---
btnCancel = InlineKeyboardButton(text='🙅‍♂️ Отмена', callback_data='cancel')
cancelPrompt = InlineKeyboardMarkup(inline_keyboard=[[btnCancel]])


# --- Confirmation prompt ---
btnYes = InlineKeyboardButton(text='✅ Да', callback_data='yes')
btnNo = InlineKeyboardButton(text='❌ Нет', callback_data='no')
confirmationPrompt = InlineKeyboardMarkup(inline_keyboard=[[btnYes,btnNo]])

# --- Admin Menu ---
btnForceEnd = InlineKeyboardButton(text='Принудительно закончить стирку', callback_data='force_end')
btnForceBreak = InlineKeyboardButton(text='Поломка',callback_data='force_break')
btnFix = InlineKeyboardButton(text='Починка', callback_data='fix')
btnKick = InlineKeyboardButton(text='Исключить пол-я', callback_data='kick')
btnBan = InlineKeyboardButton(text='Забанить пол-я', callback_data='ban')
adminMenu = InlineKeyboardMarkup(inline_keyboard=[[btnForceEnd], [btnForceBreak,btnFix], [btnKick, btnBan]])
