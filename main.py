from os import environ
from asyncio import get_event_loop
from logging import basicConfig, INFO

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import start, search

load_dotenv()


async def main():
    bot = Bot(environ.get("TOKEN"))
    dp = Dispatcher()
    dp.include_routers(start.router, search.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    basicConfig(level=INFO)
    loop = get_event_loop()
    loop.run_until_complete(main())
