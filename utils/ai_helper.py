import requests
import json
from config import GEMINI_API_KEY

def analyze_token(symbol: str, timeframe: str, data: dict) -> str:
    prompt = (
        f"Berikan analisis komprehensif untuk {symbol}/USDT dalam timeframe {timeframe}. "
        f"Data saat ini: {json.dumps(data)}."
    )
    url = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    body = {"prompt": {"text": prompt}, "temperature": 0.7, "candidateCount": 1}
    res = requests.post(url, headers=headers, params=params, json=body)
    res.raise_for_status()
    gen = res.json()
    return gen["candidates"][0]["output"]
