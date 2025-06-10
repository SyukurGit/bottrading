import requests
from config import COINGECKO_API_URL

def get_token_data(symbol: str, timeframe: str):
    # Simple fetch: current price and 24h change
    params = {
        "ids": symbol.lower(),
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    res = requests.get(f"{COINGECKO_API_URL}/simple/price", params=params)
    res.raise_for_status()
    return res.json().get(symbol.lower(), {})
