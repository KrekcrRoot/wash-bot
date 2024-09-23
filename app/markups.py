import app.texts as t
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

btnStatus = KeyboardButton(text=t.menu_status)

# --- Main Menu ---
btnHelp = KeyboardButton(text=t.menu_help)
mainMenu = ReplyKeyboardMarkup(keyboard=[[btnStatus, btnHelp]],resize_keyboard=True)

# --- Admin Main Menu ---
btnHelpAdmin = KeyboardButton(text=t.menu_help)
btnAdminMenu = KeyboardButton(text=t.menu_admin)
mainMenuAdmin = ReplyKeyboardMarkup(keyboard=[[btnStatus, btnHelpAdmin],[btnAdminMenu]],resize_keyboard=True)

# -- Report Menu --
btnForgotten = InlineKeyboardButton(text=t.menu_report_forgotten, callback_data='forgotten')
btnOccupied = InlineKeyboardButton(text=t.menu_report_occupied, callback_data='occupied')
btnBreak = InlineKeyboardButton(text=t.menu_report_break,callback_data='break')
reportMenu = InlineKeyboardMarkup(inline_keyboard=[[btnForgotten],[btnOccupied],[btnBreak]])

# --- Machine selection Menu ---
def machineMenu(machineList):
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=i.title) for i in machineList]],resize_keyboard=True)

# --- Status Menu ---
btnReport = InlineKeyboardButton(text=t.menu_report, callback_data='report')
#occupy menu
btnOccupy = InlineKeyboardButton(text=t.menu_status_occupy,callback_data='occupy')
occupyMenu = InlineKeyboardMarkup(inline_keyboard=[[btnOccupy],[btnReport]])
#queue menu
btnQueue = InlineKeyboardButton(text=t.menu_status_join_queue,callback_data='queue')
queueMenu = InlineKeyboardMarkup(inline_keyboard=[[btnQueue]])
#in queue menu
btnFree = InlineKeyboardButton(text=t.menu_status_leave_queue,callback_data='free')
in_queueMenu = InlineKeyboardMarkup(inline_keyboard=[[btnFree]])
#end menu
btnEnd = InlineKeyboardButton(text=t.menu_status_end,callback_data='end')
endMenu = InlineKeyboardMarkup(inline_keyboard=[[btnEnd],[btnReport]])

# --- Forgotten cloth prompt ---
btnCancel = InlineKeyboardButton(text=t.menu_cancel, callback_data='cancel')
cancelPrompt = InlineKeyboardMarkup(inline_keyboard=[[btnCancel]])


# --- Confirmation prompt ---
btnYes = InlineKeyboardButton(text=t.menu_yes, callback_data='yes')
btnNo = InlineKeyboardButton(text=t.menu_no, callback_data='no')
confirmationPrompt = InlineKeyboardMarkup(inline_keyboard=[[btnYes,btnNo]])

# --- Admin Menu ---
btnAddUser = InlineKeyboardButton(text=t.menu_admin_add_user, callback_data='add_user')
btnKickUser = InlineKeyboardButton(text=t.menu_admin_kick_user, callback_data='kick_user')
btnStopMachine = InlineKeyboardButton(text=t.menu_admin_stop_machine, callback_data='stop_machine')
btnForceEnd = InlineKeyboardButton(text=t.menu_admin_end, callback_data='force_end')
btnFix = InlineKeyboardButton(text=t.menu_admin_fix, callback_data='fix')
btnChangeTitle = InlineKeyboardButton(text=t.menu_admin_change_title, callback_data='change_title')
btnChangeAdmin = InlineKeyboardButton(text=t.menu_admin_change_admin, callback_data='change_admin')
adminMenu = InlineKeyboardMarkup(inline_keyboard=[[btnAddUser,btnKickUser],[btnFix],[btnForceEnd], [btnStopMachine], [btnChangeTitle], [btnChangeAdmin]])
