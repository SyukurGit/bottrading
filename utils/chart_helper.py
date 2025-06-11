# utils/chart_helper.py

import pandas as pd
import mplfinance as mpf
import io

def generate_candlestick_chart(kline_data: list, token: str, timeframe_display: str, hlines_data=None, alines_data=None):
    if not kline_data:
        return None
    try:
        df = pd.DataFrame(kline_data)
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df.set_index('time', inplace=True)
        df = df[['open', 'high', 'low', 'close', 'volume']].apply(pd.to_numeric)

        chart_title = f"\n{token.upper()}/USDT - {timeframe_display}"
        plot_kwargs = {
            "type": 'candle',
            "style": 'charles',
            "title": chart_title,
            "ylabel": 'Harga (USD)',
            "volume": True,
            "mav": (10, 20),
            "figratio": (24, 12),
            "scale_padding": 0.3,
            "warn_too_much_data": 99999,
            "tight_layout": True,
        }

        if hlines_data:
            # Menggunakan nama parameter yang benar: 'linestyle' (tanpa 's')
            hlines_data['linestyle'] = hlines_data.pop('linestyles')
            plot_kwargs['hlines'] = hlines_data
        
        if alines_data:
            plot_kwargs['alines'] = alines_data

        buf = io.BytesIO()
        mpf.plot(df, **plot_kwargs, savefig=dict(fname=buf, dpi=120, pad_inches=0.1))
        
        buf.seek(0)
        return buf
    except Exception as e:
        print(f"Gagal membuat chart: {e}")
        return None