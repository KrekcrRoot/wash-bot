from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

btnStatus = KeyboardButton(text='Status')
btnHelp = KeyboardButton(text='Help')
btnHelpAdmin = KeyboardButton(text='Help')

# --- Main Menu ---
mainMenu = ReplyKeyboardMarkup(keyboard=[[btnStatus, btnHelp]],resize_keyboard=True)

# --- Admin Main Menu ---
btnAdminMenu = KeyboardButton(text='Admin menu')
mainMenuAdmin = ReplyKeyboardMarkup(keyboard=[[btnStatus, btnAdminMenu, btnHelpAdmin]],resize_keyboard=True)


# --- Status Menu ---
btnQueue = InlineKeyboardButton(text='Queue',callback_data='queue')
btnEnd =InlineKeyboardButton(text='End',callback_data='end')
StatusMenu = InlineKeyboardMarkup(inline_keyboard=[[btnQueue]])

# --- Admin Menu ---
btnForceEnd = KeyboardButton(text='Force end')
btnBreak = KeyboardButton(text='Break')
btnFix = KeyboardButton(text='Fix')
btnKick = KeyboardButton(text='Kick')
btnBan = KeyboardButton(text='Ban')
btnMainMenuAdmin = KeyboardButton(text='Main menu')
adminMenu = ReplyKeyboardMarkup(keyboard=[[btnStatus,  btnForceEnd, btnBreak, btnFix, btnKick, btnBan, btnMainMenuAdmin, btnHelpAdmin]],resize_keyboard=True)
