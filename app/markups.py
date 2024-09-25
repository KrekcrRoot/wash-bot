import app.texts as t
from app.dto.callback_codes import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

btnStatus = KeyboardButton(text=t.menu_status)

# --- Confirmation prompts ---
btnYes = InlineKeyboardButton(text=t.menu_yes, callback_data=CallbackData.yes)
btnNo = InlineKeyboardButton(text=t.menu_no, callback_data=CallbackData.no)
confirmationPrompt = InlineKeyboardMarkup(inline_keyboard=[[btnYes,btnNo]])
btnCancel = InlineKeyboardButton(text=t.menu_cancel, callback_data=CallbackData.cancel)
cancelPrompt = InlineKeyboardMarkup(inline_keyboard=[[btnCancel]])

# --- Main Menu ---
btnHelp = KeyboardButton(text=t.menu_help)
mainMenu = ReplyKeyboardMarkup(keyboard=[[btnStatus, btnHelp]],resize_keyboard=True)

# --- Admin Main Menu ---
btnHelpAdmin = KeyboardButton(text=t.menu_help)
btnAdminMenu = KeyboardButton(text=t.menu_admin)
mainMenuAdmin = ReplyKeyboardMarkup(keyboard=[[btnStatus, btnHelpAdmin],[btnAdminMenu]],resize_keyboard=True)

# -- Report Menu --
btnForgotten = InlineKeyboardButton(text=t.menu_report_forgotten, callback_data=CallbackData.forgotten)
btnOccupied = InlineKeyboardButton(text=t.menu_report_occupied, callback_data=CallbackData.occupied)
btnBreak = InlineKeyboardButton(text=t.menu_report_break,callback_data=CallbackData.broke)
reportMenu = InlineKeyboardMarkup(inline_keyboard=[[btnForgotten],[btnOccupied],[btnBreak]])

# --- Machine selection Menu ---
def machineMenu(machineList):
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=i.title) for i in machineList]],resize_keyboard=True)

# --- Status Menu ---
btnReport = InlineKeyboardButton(text=t.menu_report, callback_data=CallbackData.report)
#occupy menu
btnOccupy = InlineKeyboardButton(text=t.menu_status_occupy,callback_data=CallbackData.occupy)
occupyMenu = InlineKeyboardMarkup(inline_keyboard=[[btnOccupy],[btnReport]])
#queue menu
btnQueue = InlineKeyboardButton(text=t.menu_status_join_queue,callback_data=CallbackData.queue)
queueMenu = InlineKeyboardMarkup(inline_keyboard=[[btnQueue]])
#in queue menu
btnFree = InlineKeyboardButton(text=t.menu_status_leave_queue,callback_data=CallbackData.free)
in_queueMenu = InlineKeyboardMarkup(inline_keyboard=[[btnFree]])
#waiting menu
btnOccupy_from_queue = InlineKeyboardButton(text=t.menu_status_occupy_from_queue, callback_data=CallbackData.occupy_from_queue)
waitingMenu = InlineKeyboardMarkup(inline_keyboard=[[btnOccupy_from_queue],[btnCancel]])
#end menu
btnEnd = InlineKeyboardButton(text=t.menu_status_end,callback_data=CallbackData.end)
endMenu = InlineKeyboardMarkup(inline_keyboard=[[btnEnd],[btnReport]])

# --- Admin Menu ---
btnAddUser = InlineKeyboardButton(text=t.menu_admin_add_user, callback_data=CallbackData.add_user)
btnKickUser = InlineKeyboardButton(text=t.menu_admin_kick_user, callback_data=CallbackData.kick_user)
btnStopMachine = InlineKeyboardButton(text=t.menu_admin_stop_machine, callback_data=CallbackData.stop_machine)
btnForceEnd = InlineKeyboardButton(text=t.menu_admin_end, callback_data=CallbackData.force_end)
btnFix = InlineKeyboardButton(text=t.menu_admin_fix, callback_data=CallbackData.fix)
btnChangeTitle = InlineKeyboardButton(text=t.menu_admin_change_title, callback_data=CallbackData.change_title)
btnChangeAdmin = InlineKeyboardButton(text=t.menu_admin_change_admin, callback_data=CallbackData.change_admin)
adminMenu = InlineKeyboardMarkup(inline_keyboard=[[btnAddUser,btnKickUser],[btnFix],[btnForceEnd], [btnStopMachine], [btnChangeTitle], [btnChangeAdmin]])
