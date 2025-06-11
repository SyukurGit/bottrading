# handlers/token_select.py

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ConversationHandler

# Impor fungsi start untuk dipanggil
from .start import start

TOKENS = ["BTC", "ETH", "BNB", "SOL"]

# Definisikan state yang relevan di sini untuk kejelasan
SELECTING_ACTION = 0
SELECTING_TOKEN = 1
SELECTING_TIMEFRAME = 2

async def token_prompt(update: Update, context):
    """Menampilkan pilihan token kepada pengguna."""
    keyboard = [TOKENS, ["🔍 Masukkan Simbol Token"], ["🔙 Kembali ke Menu Utama"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Pilih token dari tombol di bawah, atau pilih 'Masukkan Simbol Token' untuk mengetik manual:", reply_markup=reply_markup)
    return SELECTING_TOKEN # Lanjut ke state pemilihan token

async def token_select(update: Update, context):
    """Memproses token yang dipilih pengguna atau tombol lainnya."""
    text = update.message.text.strip().upper()
    
    # Kondisi untuk menangani tombol kembali
    if text == '🔙 KEMBALI KE MENU UTAMA':
        await start(update, context)
        return SELECTING_ACTION 

    # ===== BLOK PERBAIKAN DIMULAI DI SINI =====

    # Kondisi baru untuk menangani tombol input manual
    elif text == '🔍 MASUKKAN SIMBOL TOKEN':
        await update.message.reply_text("Baik, silakan ketik simbol token yang ingin Anda analisis (contoh: DOGE, XRP, ADA):")
        # Tetap di state ini untuk menunggu input teks dari pengguna
        return SELECTING_TOKEN

    # Jika bukan tombol kembali atau tombol input, baru proses sebagai nama token
    else:
        context.user_data['token'] = text
        from handlers.timeframe_select import timeframe_prompt
        await timeframe_prompt(update, context)
        # Lanjut ke state pemilihan timeframe
        return SELECTING_TIMEFRAME
        
    # ===== BLOK PERBAIKAN SELESAI =====