from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

btnStatus = KeyboardButton(text='📶 Статус')
btnHelp = KeyboardButton(text='❓ Помощь')
btnHelpAdmin = KeyboardButton(text='❓ Помощь')

# --- Main Menu ---
mainMenu = ReplyKeyboardMarkup(keyboard=[[btnStatus, btnHelp]],resize_keyboard=True)

# --- Admin Main Menu ---
btnAdminMenu = KeyboardButton(text='🛠️ Admin menu')
mainMenuAdmin = ReplyKeyboardMarkup(keyboard=[[btnStatus, btnAdminMenu, btnHelpAdmin]],resize_keyboard=True)


# --- Status Menu ---
#queue menu
btnQueue = InlineKeyboardButton(text='⏳ Занять очередь',callback_data='queue')
queueMenu = InlineKeyboardMarkup(inline_keyboard=[[btnQueue]])
#end menu
btnEnd =InlineKeyboardButton(text='🏁 Закончить стирку',callback_data='end')
btnBreak = InlineKeyboardButton(text='🔧 Поломка',callback_data='break')
endMenu = InlineKeyboardMarkup(inline_keyboard=[[btnEnd],[btnBreak]])

# --- Admin Menu ---
btnForceEnd = KeyboardButton(text='Принудительно закончить стирку')
btnFix = KeyboardButton(text='Машинка починена')
btnKick = KeyboardButton(text='Исключить пользователя')
btnBan = KeyboardButton(text='Забанить пользователя')
btnMainMenuAdmin = KeyboardButton(text='Главное меню')
adminMenu = ReplyKeyboardMarkup(keyboard=[[btnStatus], [btnForceEnd], [btnFix], [btnKick], [btnBan], [btnMainMenuAdmin], [btnHelpAdmin]],resize_keyboard=True)
