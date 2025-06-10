from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import MessageHandler, filters

TOKENS = ["BTC", "ETH", "BNB", "SOLANA"]

async def token_select(update: Update, context):
    text = update.message.text.strip().upper()
    if text == "▶️ MULAI":
        keyboard = [[" | ".join(TOKENS)], ["🔍 Masukkan Simbol Token"], ["🔙 Kembali ke Menu Utama"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Pilih token:", reply_markup=reply_markup)
    elif text in TOKENS or text.isalpha():
        context.user_data['token'] = text
        from handlers.timeframe_select import timeframe_prompt
        await timeframe_prompt(update, context)

def register_token_select(app):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, token_select))
