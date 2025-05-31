import hmac
import hashlib
import time
import requests
import json

API_KEY = "mx0vglSFP0y6ypr7Dl"
API_SECRET = "55e276ea2ffc4bb2b2752b4a2906a849"

BASE_URL = "https://api.mexc.com"

def get_timestamp():
    return str(int(time.time() * 1000))

def sign(params: dict):
    query_string = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    return signature

def place_order(symbol, side, price, stop_loss, take_profit, quantity):
    endpoint = "/api/v1/private/order/submit"
    url = BASE_URL + endpoint

    timestamp = get_timestamp()
    
    data = {
        "apiKey": API_KEY,
        "timestamp": timestamp,
        "symbol": symbol,
        "price": str(price),
        "vol": str(quantity),
        "side": side,
        "type": 1,  # 1 = limit order
        "open_type": 1,
        "position_id": 0,
        "leverage": 100,
        "external_oid": str(int(time.time())),
        "stop_loss_price": str(stop_loss),
        "take_profit_price": str(take_profit),
        "position_mode": 1,
        "reduce_only": False
    }

    data["sign"] = sign(data)

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        print(f"✅ Order Response: {response.text}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Order Failed: {e}")
        return None