# utils/api_helper.py

import requests
from config import COINGECKO_API_URL

# KAMUS UNTUK MAPPING SIMBOL KE ID COINGECKO
COINGECKO_ID_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "BNB": "binancecoin",
    "SOLANA": "solana"
}

def get_token_data(symbol: str, timeframe: str):
    """
    Mengambil data OHLC dari CoinGecko.
    Timeframe: '1h', '24h', '7d'
    """
    days_map = {
        '1h': '1',
        '24h': '1',
        '7d': '7',
    }
    days = days_map.get(timeframe, '1')

    # GUNAKAN MAPPING UNTUK MENDAPATKAN ID YANG BENAR
    # Jika simbol ada di map, gunakan ID-nya. Jika tidak, coba gunakan simbol lowercase (untuk token kustom)
    token_id = COINGECKO_ID_MAP.get(symbol.upper(), symbol.lower())

    params = {
        'vs_currency': 'usd',
        'days': days
    }
    
    # URL sekarang akan menggunakan ID yang benar (misal: 'bitcoin' bukan 'btc')
    res = requests.get(f"{COINGECKO_API_URL}/coins/{token_id}/ohlc", params=params)
    res.raise_for_status()
    return res.json()