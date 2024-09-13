from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

btnStatus = KeyboardButton(text='📶 Статус')

# --- Main Menu ---
btnHelp = KeyboardButton(text='❓ Помощь')
mainMenu = ReplyKeyboardMarkup(keyboard=[[btnStatus, btnHelp]],resize_keyboard=True)

# --- Admin Main Menu ---
btnHelpAdmin = KeyboardButton(text='❓ Помощь')
btnAdminMenu = KeyboardButton(text='🛠️ Admin menu')
mainMenuAdmin = ReplyKeyboardMarkup(keyboard=[[btnStatus, btnAdminMenu, btnHelpAdmin]],resize_keyboard=True)


# --- Status Menu ---
#queue menu
btnQueue = InlineKeyboardButton(text='⏳ Занять очередь',callback_data='queue')
queueMenu = InlineKeyboardMarkup(inline_keyboard=[[btnQueue]])
#end menu
btnEnd = InlineKeyboardButton(text='🏁 Закончить стирку',callback_data='end')
btnBreak = InlineKeyboardButton(text='🔧 Поломка',callback_data='break')
endMenu = InlineKeyboardMarkup(inline_keyboard=[[btnEnd],[btnBreak]])

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
