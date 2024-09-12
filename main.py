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
from aiogram.types import Message, BotCommand
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
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=nav.mainMenu)

@dp.message(Command("status"))
async def status(message: Message) -> None:
    await message.answer(text=f"Your ID is {message.from_user.id}",reply_markup=nav.StatusMenu)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    result: bool = await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Объяснение команд"),
        BotCommand(command="status", description="Получить статус")
    ])
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())