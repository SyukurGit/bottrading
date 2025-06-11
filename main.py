# main.py

import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# Impor fungsi handler Anda
from handlers.start import start
from handlers.token_select import token_prompt, token_select
from handlers.timeframe_select import timeframe_select
from handlers.analysis import start_analysis_callback
from utils.db import init_db
# ===== PERUBAHAN DIMULAI DI SINI =====
from utils.coin_list import load_coin_list
# ===== PERUBAHAN SELESAI =====

# Definisikan state untuk ConversationHandler
SELECTING_ACTION, SELECTING_TOKEN, SELECTING_TIMEFRAME = range(3)

def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    
    # ===== PERUBAHAN DIMULAI DI SINI =====
    # Muat daftar koin dari CoinGecko ke memori saat bot start
    load_coin_list()
    # ===== PERUBAHAN SELESAI =====
    
    init_db()
    app = ApplicationBuilder().token("7207657126:AAF53TTiNB_VIQcl_8bk5DfYKgZ6laX8izU").build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex('^Pilih Token Lain$'), token_prompt)
        ],
        states={
            SELECTING_ACTION: [
                MessageHandler(filters.Regex('^▶️ Mulai$'), token_prompt)
            ],
            SELECTING_TOKEN: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, token_select)
            ],
            SELECTING_TIMEFRAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, timeframe_select)
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(start_analysis_callback, pattern="start_analysis"))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()