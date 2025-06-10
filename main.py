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

# Definisikan state untuk ConversationHandler
SELECTING_ACTION, SELECTING_TOKEN, SELECTING_TIMEFRAME = range(3)

def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    init_db()
    # Pastikan untuk mengganti token dengan token Anda yang sebenarnya
    app = ApplicationBuilder().token("7207657126:AAF53TTiNB_VIQcl_8bk5DfYKgZ6laX8izU").build()

    # Buat ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECTING_ACTION: [
                MessageHandler(filters.Regex('^▶️ Mulai$'), token_prompt)
            ],
            SELECTING_TOKEN: [
                # Menggunakan filter teks biasa karena bisa jadi token kustom
                MessageHandler(filters.TEXT & ~filters.COMMAND, token_select)
            ],
            SELECTING_TIMEFRAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, timeframe_select)
            ],
        },
        fallbacks=[CommandHandler("start", start)], # Jika pengguna bingung, bisa /start ulang
    )

    app.add_handler(conv_handler)
    
    # Handler untuk analisis tetap di luar conversation karena menggunakan InlineKeyboard
    app.add_handler(CallbackQueryHandler(start_analysis_callback, pattern="start_analysis"))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()