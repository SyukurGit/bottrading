# handlers/analysis.py
from telegram.ext import CallbackQueryHandler
from utils.cooldown import is_on_cooldown, update_cooldown
from utils.api_helper import get_token_data
from utils.ai_helper import analyze_token
from utils.chart_helper import generate_candlestick_chart # Impor fungsi chart

async def start_analysis_callback(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    
    if is_on_cooldown(user_id):
        await query.answer("⚠️ Anda harus menunggu selama 3 menit untuk melanjutkan analisanya.", show_alert=True)
        return
        
    await query.answer("Sedang memproses... mohon tunggu sebentar.")
    
    try:
        token = context.user_data.get('token')
        timeframe_display = [k for k, v in context.user_data.get('TIMEFRAMES', {}).items() if v == context.user_data.get('timeframe')][0]
        timeframe_value = context.user_data.get('timeframe')

        if not token or not timeframe_value:
            await query.message.reply_text("❌ Terjadi kesalahan: Token atau timeframe tidak ditemukan. Silakan mulai ulang dengan /start.")
            return

        # 1. Ambil data OHLC dari CoinGecko
        ohlc_data = get_token_data(token, timeframe_value)
        if not ohlc_data:
            await query.message.reply_text(f"Gagal mendapatkan data untuk {token}. Mungkin token tidak didukung CoinGecko.")
            return

        # 2. Buat dan kirim gambar chart
        chart_image = generate_candlestick_chart(ohlc_data, token, timeframe_display)
        if chart_image:
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=chart_image,
                caption=f"Chart Candlestick untuk {token.upper()}/USDT ({timeframe_display})"
            )
        else:
            await context.bot.send_message(chat_id=query.message.chat_id, text="Gagal membuat chart.")

        # 3. Analisis dengan AI
        await context.bot.send_message(chat_id=query.message.chat_id, text="Menganalisis data dengan AI...")
        result = analyze_token(token, timeframe_display, ohlc_data) # Kirim data OHLC ke AI
        
        # 4. Kirim hasil analisis
        await query.message.reply_text(result)
        update_cooldown(user_id)

    except Exception as e:
        print(f"An error occurred in start_analysis_callback: {e}")
        await query.message.reply_text(f"Terjadi kesalahan tak terduga saat melakukan analisis. Silakan coba lagi.\n\nDetail: {e}")

def register_analysis(app):
    app.add_handler(CallbackQueryHandler(start_analysis_callback, pattern="start_analysis"))