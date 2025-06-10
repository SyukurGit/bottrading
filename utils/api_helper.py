# utils/api_helper.py

import requests

# URL API resmi dari Binance
BINANCE_API_URL = "https://api.binance.com/api/v3/klines"

def get_binance_kline_data(symbol: str, timeframe: str):
    """
    Mengambil data Kline (OHLCV) dari Binance API.
    """
    # Mapping timeframe kita ke interval yang dimengerti Binance
    interval_map = {
        '1h': '1h',   # 1 Jam
        '24h': '4h',  # Untuk 24 jam, kita ambil data 4-jam-an agar tidak terlalu padat
        '7d': '1d',   # Untuk Long Term, kita ambil data harian
    }
    interval = interval_map.get(timeframe, '1h')
    
    # Binance menggunakan format simbol seperti 'BTCUSDT'
    formatted_symbol = symbol.upper() + "USDT"

    # Ambil 100 candle terakhir untuk interval yang dipilih
    params = {
        'symbol': formatted_symbol,
        'interval': interval,
        'limit': 100 
    }
    
    try:
        res = requests.get(BINANCE_API_URL, params=params)
        res.raise_for_status()
        
        # Binance memberikan data dalam format list. Kita perlu memformatnya.
        # [open_time, open, high, low, close, volume, ...]
        processed_data = []
        for kline in res.json():
            processed_data.append({
                "time": kline[0],
                "open": float(kline[1]),
                "high": float(kline[2]),
                "low": float(kline[3]),
                "close": float(kline[4]),
                "volume": float(kline[5])
            })
        return processed_data
    except requests.exceptions.RequestException as e:
        print(f"Gagal mengambil data dari Binance: {e}")
        return None