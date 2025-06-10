from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, filters

TIMEFRAMES = {"1 Jam": "1h", "24 Jam": "24h", "Long Term": "7d"}

async def timeframe_prompt(update: Update, context):
    keyboard = [["1 Jam", "24 Jam", "Long Term"], ["🔙 Kembali ke Pemilihan Token"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Pilih timeframe:", reply_markup=reply_markup)

async def timeframe_select(update: Update, context):
    text = update.message.text.strip()
    if text in TIMEFRAMES:
        context.user_data['timeframe'] = TIMEFRAMES[text]
        token = context.user_data.get('token')
        await update.message.reply_text(f"🔎 Analisis {token}/USDT ({text})")
        button = InlineKeyboardButton("🚀 Start Analysis", callback_data="start_analysis")
        markup = InlineKeyboardMarkup([[button]])
        await update.message.reply_text("Klik untuk memulai analisis:", reply_markup=markup)

def register_timeframe_select(app):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, timeframe_select))
