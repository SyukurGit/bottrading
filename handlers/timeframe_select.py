# handlers/timeframe_select.py

from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

TIMEFRAMES = {"1 Jam": "1h", "24 Jam": "24h", "Long Term": "7d"}

async def timeframe_prompt(update: Update, context):
    """Menampilkan pilihan timeframe."""
    keyboard = [["1 Jam", "24 Jam", "Long Term"], ["🔙 Kembali ke Pemilihan Token"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Pilih timeframe:", reply_markup=reply_markup)

async def timeframe_select(update: Update, context):
    """Memproses timeframe yang dipilih."""
    text = update.message.text.strip()

    # Simpan TIMEFRAMES ke context untuk digunakan nanti
    context.user_data['TIMEFRAMES'] = TIMEFRAMES

    if text == "🔙 Kembali ke Pemilihan Token":
        from handlers.token_select import token_prompt
        await token_prompt(update, context)
        return 1 # Kembali ke state SELECTING_TOKEN

    if text in TIMEFRAMES:
        context.user_data['timeframe'] = TIMEFRAMES[text]
        token = context.user_data.get('token')
        await update.message.reply_text(f"🔎 Analisis {token}/USDT ({text})")
        button = InlineKeyboardButton("🚀 Start Analysis", callback_data="start_analysis")
        markup = InlineKeyboardMarkup([[button]])
        await update.message.reply_text("Klik untuk memulai analisis:", reply_markup=markup)
        return ConversationHandler.END # Akhiri percakapan setelah ini
    else:
        # Jika input tidak valid, minta lagi
        await update.message.reply_text("Pilihan timeframe tidak valid. Silakan pilih dari keyboard.")
        return 2 # Tetap di state SELECTING_TIMEFRAME