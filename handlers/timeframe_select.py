# handlers/timeframe_select.py

from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from .token_select import token_prompt # Impor fungsi token_prompt

# Definisikan state secara eksplisit untuk kejelasan
# Sesuaikan angka ini jika Anda mengubah urutan state di main.py
SELECTING_TOKEN = 1
SELECTING_TIMEFRAME = 2

TIMEFRAMES = {"1 Jam": "1h", "24 Jam": "24h", "Long Term": "7d"}

async def timeframe_prompt(update: Update, context):
    """Menampilkan pilihan timeframe."""
    keyboard = [["1 Jam", "24 Jam", "Long Term"], ["🔙 Kembali ke Pemilihan Token"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Pilih timeframe:", reply_markup=reply_markup)
    # Fungsi ini tidak mengubah state, hanya menampilkan prompt

async def timeframe_select(update: Update, context):
    """Memproses timeframe yang dipilih atau tombol kembali."""
    text = update.message.text.strip()
    
    # Simpan TIMEFRAMES ke context untuk digunakan nanti di handler analisis
    context.user_data['TIMEFRAMES'] = TIMEFRAMES

    # ===== BLOK PERBAIKAN DIMULAI DI SINI =====
    
    # 1. Cek apakah pengguna menekan tombol "Kembali"
    if text == "🔙 Kembali ke Pemilihan Token":
        # Panggil kembali prompt pemilihan token
        await token_prompt(update, context)
        # Kembalikan state percakapan ke tahap pemilihan token (state 1)
        return SELECTING_TOKEN

    # 2. Jika bukan tombol kembali, cek apakah itu timeframe yang valid
    elif text in TIMEFRAMES:
        context.user_data['timeframe'] = TIMEFRAMES[text]
        token = context.user_data.get('token')
        await update.message.reply_text(f"🔎 Analisis {token}/USDT ({text})")
        button = InlineKeyboardButton("🚀 Start Analysis", callback_data="start_analysis")
        markup = InlineKeyboardMarkup([[button]])
        await update.message.reply_text("Klik untuk memulai analisis:", reply_markup=markup)
        # Akhiri percakapan karena alur utama selesai
        return ConversationHandler.END
        
    # 3. Jika input tidak valid (bukan tombol kembali atau timeframe)
    else:
        await update.message.reply_text("Pilihan tidak valid. Silakan pilih dari keyboard.")
        # Tetap di state pemilihan timeframe
        return SELECTING_TIMEFRAME

    # ===== BLOK PERBAIKAN SELESAI =====