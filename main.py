import asyncio
import logging
import sys
import os 
import markups as nav
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand, CallbackQuery
from aiogram.methods.set_my_commands import SetMyCommands

from api import API

load_dotenv()

# print(os.getenv('TOKEN'))

TOKEN = os.environ.get("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()

api_controller = API()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_is_authorized=False
    if user_is_authorized==False:
        await message.answer(text='Привет, {html(message.from_user.full_name)}!'+'\n'+'Введите полный номер своей комнаты:'+'\n'+'(например: 1501/2, 1514/3)')

@dp.message()
async def keyboardMenu_handler(message: Message) -> None:
    print(message.message_thread_id)
    if message.text == '📶 Статус':
        await message.answer(text='text',reply_markup=nav.queueMenu)

    elif message.text == '🛠️ Admin menu':
        await message.answer(text='text',reply_markup=nav.adminMenu)

    elif message.text == '❓ Помощь':
        await message.answer(text='text')
    
@dp.callback_query()
async def inlineMenu_handler(callback: CallbackQuery) -> None:
    if callback.data == 'queue':

        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.endMenu)
        await callback.answer()

    elif callback.data == 'end':

        await callback.answer(text='ended')

    elif callback.data == 'break':
        await callback.message.edit_text(text='Вы уверены?')
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.confirmationPrompt)
        await callback.answer()
    
    elif callback.data == 'yes':
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,reply_markup=nav.queueMenu)
        await callback.answer(text='broke')
    
    elif callback.data == 'no':
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