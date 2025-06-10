# utils/chart_helper.py
import pandas as pd
import mplfinance as mpf
import io

def generate_candlestick_chart(ohlc_data: list, token: str, timeframe: str):
    """
    Membuat gambar candlestick chart dari data OHLC dan mengembalikannya sebagai byte stream.
    """
    if not ohlc_data:
        return None

    try:
        # Konversi data ke pandas DataFrame
        df = pd.DataFrame(ohlc_data, columns=['time', 'open', 'high', 'low', 'close'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df.set_index('time', inplace=True)

        # Buat chart
        buf = io.BytesIO()
        chart_title = f"{token.upper()}/USDT - Timeframe: {timeframe}"
        mpf.plot(df, type='candle', style='yahoo',
                 title=chart_title,
                 ylabel='Harga (USD)',
                 volume=False, # Volume tidak kita ambil untuk saat ini
                 savefig=dict(fname=buf, dpi=100, pad_inches=0.25))
        
        buf.seek(0)
        return buf
    except Exception as e:
        print(f"Gagal membuat chart: {e}")
        return None