import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from handlers import register_handlers

API_TOKEN = "7576879160:AAFKhpZgI1YXGSQLTICLeJgo1J3z9OG8A7Q"  # توكن البوت حقك

# إعدادات اللوغ
logging.basicConfig(level=logging.INFO)

# إنشاء البوت والديسباتشر
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# تسجيل الهاندلرز
register_handlers(dp)

# تشغيل البوت
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)