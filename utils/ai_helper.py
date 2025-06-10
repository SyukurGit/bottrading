# utils/ai_helper.py

import requests
import json
from config import GEMINI_API_KEY

def analyze_token_and_get_trendlines(symbol: str, timeframe: str, kline_data: list):
    """
    Menganalisis data, memberikan teks analisis, dan juga data JSON untuk garis tren.
    """
    recent_data = kline_data[-50:] # Kirim 50 data poin terakhir ke AI
    
    prompt = f"""
    Anda adalah seorang analis teknikal trading profesional. Lakukan dua hal:
    
    1.  **Berikan Analisis Teks**: Tulis analisis komprehensif untuk pasangan {symbol}/USDT dalam timeframe {timeframe} berdasarkan data kline (OHLC) berikut. Analisis harus mencakup identifikasi tren, level support dan resistance utama, serta potensi sinyal trading.
    
    2.  **Berikan Data Garis Tren (JSON)**: Berdasarkan analisis Anda, identifikasi maksimal 2 garis tren paling signifikan (bisa support atau resistance). Sajikan data garis ini dalam format JSON yang ketat di bawah ini. Garis harus menghubungkan dua titik (titik awal dan akhir). Setiap titik didefinisikan oleh timestamp (ms) dan harga. Gunakan timestamp dari data yang diberikan.

    Berikut adalah data Kline (timestamp, open, high, low, close, volume):
    {json.dumps(recent_data, indent=2)}

    Format output WAJIB seperti ini, pisahkan analisis teks dan JSON dengan "---JSON_SEPARATOR---":

    [ANALISIS TEKS ANDA DI SINI]
    ---JSON_SEPARATOR---
    {{
      "trendlines": [
        {{
          "type": "support/resistance",
          "points": [
            {{ "timestamp": [timestamp_awal], "price": [harga_awal] }},
            {{ "timestamp": [timestamp_akhir], "price": [harga_akhir] }}
          ]
        }}
      ]
    }}

    Jika Anda tidak dapat mengidentifikasi garis tren yang jelas, kembalikan array kosong untuk "trendlines".
    """

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    body = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.5}}

    try:
        res = requests.post(url, headers=headers, json=body, timeout=45)
        res.raise_for_status()
        
        full_response_text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
        
        # Pisahkan analisis teks dan data JSON
        if "---JSON_SEPARATOR---" in full_response_text:
            parts = full_response_text.split("---JSON_SEPARATOR---", 1)
            text_analysis = parts[0].strip()
            json_str = parts[1].strip()
            
            # Parsing data JSON untuk garis tren
            try:
                trendline_data = json.loads(json_str)
                return text_analysis, trendline_data.get("trendlines", [])
            except json.JSONDecodeError:
                return text_analysis, [] # Jika JSON tidak valid, kembalikan list kosong
        else:
            return full_response_text, [] # Jika separator tidak ada

    except Exception as e:
        print(f"Error saat menghubungi Gemini API: {e}")
        return f"Terjadi kesalahan pada layanan AI: {e}", []