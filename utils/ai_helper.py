# utils/ai_helper.py

import requests
import json
from config import GEMINI_API_KEY

def analyze_token(symbol: str, timeframe: str, data: list) -> str:
    """Menganalisis data token menggunakan Gemini API v1."""
    # Ambil beberapa data poin terakhir untuk efisiensi prompt
    recent_data = data[-10:] # Ambil 10 data terakhir saja

    prompt = (
        f"Anda adalah seorang analis trading futures profesional. Berikan analisis teknikal yang komprehensif dan sinyal trading (entry, take profit, stop loss) untuk pasangan {symbol}/USDT dalam timeframe {timeframe}. "
        f"Sertakan juga sentimen pasar saat ini.\n\n"
        f"Berikut adalah data OHLC (Open, High, Low, Close) terbaru (timestamp, open, high, low, close):\n{json.dumps(recent_data, indent=2)}\n\n"
        "Gunakan data di atas untuk analisis Anda. Berikan jawaban dalam format yang jelas dan mudah dibaca dalam Bahasa Indonesia."
    )

    # URL dan Model API Gemini v1 yang baru
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    
    # Body request yang baru
    body = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024,
        }
    }

    try:
        res = requests.post(url, headers=headers, json=body, timeout=30)
        res.raise_for_status()
        
        gen = res.json()
        
        if "candidates" in gen and len(gen["candidates"]) > 0:
            if "content" in gen["candidates"][0] and "parts" in gen["candidates"][0]["content"]:
                return gen["candidates"][0]["content"]["parts"][0]["text"]
        
        return f"Gagal mem-parsing respons dari AI. Respons mentah: {json.dumps(gen)}"

    except requests.exceptions.RequestException as e:
        print(f"Error saat menghubungi Gemini API: {e}")
        return f"Terjadi kesalahan saat mencoba menghubungi layanan AI. Silakan coba lagi nanti. Error: {e}"