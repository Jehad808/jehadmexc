import asyncio
from aiogram import Bot, Dispatcher
from handlers import register_handlers
from config import TELEGRAM_BOT_TOKEN

bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

async def main():
    register_handlers(dp)
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())