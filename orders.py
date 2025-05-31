import time
import hmac
import hashlib
import requests
from config import MEXC_API_KEY, MEXC_API_SECRET, POSITION_SIZE_PERCENT, LEVERAGE

BASE_URL = "https://contract.mexc.com"

def sign(params, secret):
    query_string = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def get_balance():
    path = "/api/v1/private/account/asset/USDT"
    timestamp = int(time.time() * 1000)
    params = {
        "api_key": MEXC_API_KEY,
        "req_time": timestamp
    }
    params["sign"] = sign(params, MEXC_API_SECRET)
    response = requests.get(BASE_URL + path, params=params)
    data = response.json()
    if data.get("success"):
        return float(data["data"]["availableBalance"])
    return 0.0

def place_order(symbol, side, price, quantity):
    path = "/api/v1/private/order/submit"
    timestamp = int(time.time() * 1000)
    params = {
        "api_key": MEXC_API_KEY,
        "req_time": timestamp,
        "symbol": symbol.lower(),
        "price": price,
        "vol": quantity,
        "side": side,
        "leverage": LEVERAGE,
        "category": 1,
        "trade_type": 1,
        "position_mode": 1,
        "reduce_only": False,
        "price_type": 1,
    }
    params["sign"] = sign(params, MEXC_API_SECRET)
    response = requests.post(BASE_URL + path, data=params)
    return response.json()

async def open_position(symbol, direction, entry_price, tp1, tp2, sl, message):
    balance = get_balance()
    if balance == 0:
        await message.reply("❌ مافي رصيد كافي.")
        return

    side = 1 if direction == "long" else 2
    position_size = balance * (POSITION_SIZE_PERCENT / 100)
    quantity = round(position_size / entry_price, 4)
    response = place_order(symbol, side, entry_price, quantity)

    if response.get("success"):
        await message.reply(f"✅ تم فتح صفقة {direction.upper()} على {symbol} بحجم {quantity} عند السعر {entry_price}")
    else:
        await message.reply(f"❌ خطأ: {response.get('message')}")