# utils/chart_helper.py

import pandas as pd
import mplfinance as mpf
import io

def generate_candlestick_chart(kline_data: list, token: str, timeframe_display: str, trendlines=None):
    """
    Membuat gambar candlestick chart dari data Kline Binance.
    Bisa juga menggambar garis tren jika diberikan.
    """
    if not kline_data:
        return None

    try:
        # Konversi data ke pandas DataFrame
        df = pd.DataFrame(kline_data)
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df.set_index('time', inplace=True)

        # Siapkan argumen untuk plot
        chart_title = f"{token.upper()}/USDT - {timeframe_display}"
        plot_kwargs = {
            "type": 'candle',
            "style": 'binance', # Gunakan style yang lebih menarik
            "title": chart_title,
            "ylabel": 'Harga (USD)',
            "volume": True, # Tampilkan volume
            "mav": (10, 20), # Tambahkan Moving Average periode 10 dan 20
            "figratio": (12, 7),
            "scale_padding": 0.5
        }

        # Jika ada data trendline, tambahkan ke plot
        if trendlines:
            plot_kwargs['alines'] = trendlines

        # Buat chart
        buf = io.BytesIO()
        mpf.plot(df, **plot_kwargs, savefig=dict(fname=buf, dpi=120, pad_inches=0.25))
        
        buf.seek(0)
        return buf
    except Exception as e:
        print(f"Gagal membuat chart: {e}")
        return None