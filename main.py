import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
import multiprocessing

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiohttp import web

from app.router import router
from app.server.iostream import app
load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")
dp = Dispatcher()

async def main() -> None:
    try:
        bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        dp.include_router(router=router)
        result: bool = await bot.set_my_commands([
            BotCommand(command="start", description="Запустить бота"),
            BotCommand(command="change_machine", description="Смена стиралки"),
            BotCommand(command="cancel", description="Отменить действие"),
            BotCommand(command="info", description="Информация о пользователе"),
            BotCommand(command="help", description="Объяснение команд")
        ])
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        sys.exit(0)


def run_iostream():
    try:
        web.run_app(app)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        iostream_thread = multiprocessing.Process(target=run_iostream, args=())
        iostream_thread.start()

        asyncio.run(main())
    except KeyboardInterrupt:

        iostream_thread.terminate()

