from aiogram import types
from aiogram.dispatcher import Dispatcher
from orders import place_order
import re

CHANNEL_ID = -1002590077730  # قناة التوصيات @jehadmexc

def register_handlers(dp: Dispatcher):
    @dp.message_handler(lambda message: message.chat.id == CHANNEL_ID)
    async def handle_signal(message: types.Message):
        text = message.text

        try:
            # استخراج البيانات باستخدام Regular Expressions
            symbol_match = re.search(r"Symbol:\s*(\w+)", text)
            direction_match = re.search(r"Direction:\s*(LONG|SHORT)", text, re.IGNORECASE)
            entry_match = re.search(r"Entry Price:\s*([\d.]+)", text)
            tp1_match = re.search(r"Take Profit 1:\s*([\d.]+)", text)
            sl_match = re.search(r"Stop Loss:\s*([\d.]+)", text)

            if not all([symbol_match, direction_match, entry_match, tp1_match, sl_match]):
                print("❌ لم يتم التعرف على جميع البيانات من الرسالة.")
                return

            symbol = symbol_match.group(1).upper()
            direction = direction_match.group(1).upper()
            entry_price = float(entry_match.group(1))
            take_profit = float(tp1_match.group(1))
            stop_loss = float(sl_match.group(1))

            print(f"📥 تم استقبال توصية: {symbol} | {direction}")
            await place_order(symbol, direction, entry_price, take_profit, stop_loss)

        except Exception as e:
            print(f"⚠️ خطأ أثناء معالجة التوصية: {e}")