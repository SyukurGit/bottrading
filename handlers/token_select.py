# handlers/token_select.py

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ConversationHandler

TOKENS = ["BTC", "ETH", "BNB", "SOLANA"]

# STATE untuk ConversationHandler
SELECTING_TOKEN, SELECTING_TIMEFRAME = range(1, 3)

async def token_prompt(update: Update, context):
    """Menampilkan pilihan token kepada pengguna."""
    # UBAH BAGIAN INI: Buat satu baris yang berisi 4 tombol
    keyboard = [TOKENS, ["🔍 Masukkan Simbol Token"], ["🔙 Kembali ke Menu Utama"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Pilih token:", reply_markup=reply_markup)
    return SELECTING_TOKEN

async def token_select(update: Update, context):
    """Memproses token yang dipilih pengguna."""
    text = update.message.text.strip().upper()
    
    if text == '🔙 KEMBALI KE MENU UTAMA':
        from handlers.start import start
        await start(update, context)
        return ConversationHandler.END

    context.user_data['token'] = text
    from handlers.timeframe_select import timeframe_prompt
    await timeframe_prompt(update, context)
    return SELECTING_TIMEFRAME