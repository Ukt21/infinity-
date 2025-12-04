import asyncio
import logging
import sys

import uvloop
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from db import init_db
from routers.start import router as start_router
from routers.menu import router as menu_router
from routers.text_ai import router as text_ai_router
from routers.image_ai import router as image_ai_router
from routers.subscription import router as subscription_router
from routers.admin_panel import router as admin_router


logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


async def main():
    uvloop.install()

    init_db()

    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация роутеров
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(text_ai_router)
    dp.include_router(image_ai_router)
    dp.include_router(subscription_router)
    dp.include_router(admin_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

