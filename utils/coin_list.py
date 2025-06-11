# utils/coin_list.py

import requests
from config import COINGECKO_API_URL

# Variabel ini akan menyimpan mapping dari simbol (lowercase) ke id coingecko
# Contoh: {'btc': 'bitcoin', 'eth': 'ethereum'}
COIN_MAP = {}

def load_coin_list():
    """
    Mengunduh daftar lengkap koin dari CoinGecko dan menyimpannya ke dalam COIN_MAP.
    Fungsi ini harus dipanggil sekali saat bot startup.
    """
    global COIN_MAP
    try:
        print("Mengunduh daftar koin dari CoinGecko...")
        url = f"{COINGECKO_API_URL}/coins/list"
        res = requests.get(url, timeout=30)
        res.raise_for_status()
        coin_list = res.json()
        
        # Proses daftar dan buat mapping: simbol -> id
        # Kita utamakan id yang lebih pendek jika ada duplikasi simbol
        temp_map = {}
        for coin in coin_list:
            symbol = coin['symbol'].lower()
            coin_id = coin['id']
            # Jika simbol belum ada, atau id baru lebih pendek dari id lama
            if symbol not in temp_map or len(coin_id) < len(temp_map[symbol]):
                 temp_map[symbol] = coin_id
        
        COIN_MAP = temp_map
        print(f"Berhasil memuat {len(COIN_MAP)} token ke dalam memori.")
        
    except requests.exceptions.RequestException as e:
        print(f"KRITIS: Gagal mengunduh daftar koin dari CoinGecko: {e}")
        print("Bot mungkin tidak dapat menemukan profil koin.")
        # Kita tetap set COIN_MAP sebagai dict kosong agar bot tidak crash
        COIN_MAP = {}


def get_id_from_symbol(symbol: str) -> str | None:
    """
    Mencari ID CoinGecko dari simbol token menggunakan COIN_MAP yang sudah dimuat.
    """
    return COIN_MAP.get(symbol.lower())