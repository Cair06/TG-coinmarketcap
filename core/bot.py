import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from handlers import register_handlers
from scheduler import scheduled_check_thresholds
from database import init_db

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))


TOKEN = os.environ["BOT_TOKEN"]

dp = Dispatcher()
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)


async def main() -> None:
    await init_db()
    session = AiohttpSession()
    bot = Bot(token=TOKEN, session=session, parse_mode=ParseMode.HTML)

    # Регистрация хендлеров
    register_handlers(dp)

    # Запуск планировщика задач
    asyncio.create_task(scheduled_check_thresholds(bot))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
