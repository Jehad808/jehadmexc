import re
from aiogram import types
from aiogram.dispatcher import Dispatcher
from orders import open_position
from config import TELEGRAM_CHANNEL_ID

PATTERN = re.compile(
    r"Symbol:\s*(\w+)\s*"
    r"Direction:\s*(Long|Short)\s*"
    r"Entry Price:\s*([\d\.]+)\s*"
    r"Take Profit 1:\s*([\d\.]+)\s*"
    r"Take Profit 2:\s*([\d\.]+)\s*"
    r"Stop Loss:\s*([\d\.]+)", re.IGNORECASE
)

async def channel_handler(message: types.Message):
    if message.chat.id != TELEGRAM_CHANNEL_ID:
        return

    text = message.text or message.caption or ""
    match = PATTERN.search(text)
    if not match:
        return

    symbol = match.group(1).upper()
    direction = match.group(2).lower()
    entry_price = float(match.group(3))
    tp1 = float(match.group(4))
    tp2 = float(match.group(5))
    sl = float(match.group(6))

    await open_position(symbol, direction, entry_price, tp1, tp2, sl, message)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(channel_handler, content_types=types.ContentType.TEXT)