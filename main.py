import asyncio
import logging
import sys
import os
import re 
import markups as nav
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand, CallbackQuery
from aiogram.methods.set_my_commands import SetMyCommands
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from api import API

load_dotenv()

# print(os.getenv('TOKEN'))

TOKEN = os.environ.get("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()

api_controller = API()

class Form(StatesGroup):
    machineSelect = State()

#Returning inline menu into status menu
async def return_to_statusMenu(callback: CallbackQuery) -> None:
    status='free'
    if status=='free':
        await callback.message.edit_text(text='text')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.occupyMenu)
    elif status=='in work':
        await callback.message.edit_text(text='text')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.queueMenu)
    else:
        await callback.message.edit_text(text='Занято')
        await callback.message.delete_reply_markup()
        

#Authorization thing
@dp.message(CommandStart())
async def command_start_handler(message: Message, state:FSMContext) -> None:
    user_is_authorized=True
    if user_is_authorized==True:
        machines_list=[['machine']]
        if len(machines_list)==1:
            user_is_admin=False
            if user_is_admin:
                await message.answer(text='text',reply_markup=nav.mainMenuAdmin)
            await message.answer(text='text',reply_markup=nav.mainMenu)

#Handling keyboard menu actions
@dp.message()
async def keyboardMenu_handler(message: Message) -> None:
    if message.text == '📶 Статус':
        status='free'
        if status=='free':
            await message.answer(text='text',reply_markup=nav.occupyMenu)
        elif status=='in work':
            await message.answer(text='text',reply_markup=nav.queueMenu)
        else:
            await message.answer(text='Занято')
    elif message.text == '🛠️ Admin menu':
        await message.answer(text='text',reply_markup=nav.adminMenu)

    elif message.text == '❓ Помощь':
        await message.answer(text='text')

#Handling inline menu actions
@dp.callback_query()
async def inlineMenu_handler(callback: CallbackQuery) -> None:

    if callback.data == 'occupy':
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.endMenu)
        await callback.answer()

    elif callback.data == 'queue':
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.in_queueMenu)
        await callback.answer()

    elif callback.data == 'free':
        await return_to_statusMenu(callback)
        await callback.answer()

    elif callback.data == 'end':
        await return_to_statusMenu(callback)
        await callback.answer(text='ended')
    
    elif callback.data == 'forgotten':
        await callback.answer(text='forgotten')

    elif callback.data == 'break':
        await callback.message.edit_text(text='Вы уверены?')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.confirmationPrompt)
        await callback.answer()
    
    elif callback.data == 'yes':
        await return_to_statusMenu(callback)
        await callback.answer(text='broke')
    
    elif callback.data == 'no':
        await callback.message.edit_text(text='text')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.endMenu)
        await callback.answer()

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    result: bool = await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Объяснение команд"),
    ])
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())