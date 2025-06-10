# handlers/analysis.py

from telegram import ReplyKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from utils.cooldown import is_on_cooldown, update_cooldown
# Ganti import helper
from utils.api_helper import get_binance_kline_data
from utils.ai_helper import analyze_token_and_get_trendlines
from utils.chart_helper import generate_candlestick_chart

async def start_analysis_callback(update, context):
    query = update.callback_query
    await query.answer("Sedang memproses... ini mungkin butuh waktu lebih lama.")
    
    try:
        user_id = query.from_user.id
        if is_on_cooldown(user_id):
            # Cek cooldown lagi jika ada jeda
            await query.edit_message_text("⚠️ Anda harus menunggu cooldown selesai.")
            return

        token = context.user_data.get('token')
        timeframe_value = context.user_data.get('timeframe')
        timeframe_display_map = context.user_data.get('TIMEFRAMES', {})
        timeframe_display = [k for k, v in timeframe_display_map.items() if v == timeframe_value][0] or timeframe_value

        # 1. Ambil data detail dari Binance
        await query.edit_message_text(f"Mengambil data detail untuk {token}...")
        kline_data = get_binance_kline_data(token, timeframe_value)
        if not kline_data:
            await query.edit_message_text(f"Gagal mendapatkan data dari Binance untuk {token}.")
            return

        # 2. Buat dan kirim chart PERTAMA (tanpa garis tren)
        await query.edit_message_text("Membuat chart awal...")
        clean_chart_image = generate_candlestick_chart(kline_data, token, timeframe_display)
        if clean_chart_image:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=clean_chart_image, caption=f"Chart Awal untuk {token.upper()}/USDT ({timeframe_display})")
        
        # 3. Analisis dengan AI untuk mendapatkan teks & garis tren
        await context.bot.send_message(chat_id=query.message.chat_id, text="Menganalisis dengan AI untuk mencari tren...")
        text_analysis, trendlines_json = analyze_token_and_get_trendlines(token, timeframe_display, kline_data)

        # 4. Kirim hasil analisis TEKS
        await context.bot.send_message(chat_id=query.message.chat_id, text=text_analysis)

        # 5. Jika AI memberikan garis tren, buat dan kirim chart KEDUA
        if trendlines_json:
            await context.bot.send_message(chat_id=query.message.chat_id, text="Membuat chart dengan garis tren...")
            # Format data garis untuk mplfinance
            alines_data = []
            for line in trendlines_json:
                points = line.get("points", [])
                if len(points) == 2:
                    start_point = (pd.to_datetime(points[0]['timestamp'], unit='ms'), points[0]['price'])
                    end_point = (pd.to_datetime(points[1]['timestamp'], unit='ms'), points[1]['price'])
                    alines_data.append([start_point, end_point])

            if alines_data:
                trend_chart_image = generate_candlestick_chart(kline_data, token, timeframe_display, trendlines=alines_data)
                if trend_chart_image:
                    await context.bot.send_photo(chat_id=query.message.chat_id, photo=trend_chart_image, caption="Chart dengan Analisis Garis Tren")

        update_cooldown(user_id)
        
        # 6. Kirim tombol untuk memulai lagi
        keyboard = [["Pilih Token Lain"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await context.bot.send_message(chat_id=query.message.chat_id, text="Analisis selesai.", reply_markup=reply_markup)

    except Exception as e:
        print(f"An error occurred in start_analysis_callback: {e}")
        await context.bot.send_message(chat_id=query.message.chat_id, text=f"Terjadi kesalahan tak terduga: {e}")