import logging
from telegram.ext import ApplicationBuilder
from handlers.start import register_start
from handlers.token_select import register_token_select
from handlers.timeframe_select import register_timeframe_select
from handlers.analysis import register_analysis
from utils.db import init_db

def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    init_db()
    app = ApplicationBuilder().token("7207657126:AAF53TTiNB_VIQcl_8bk5DfYKgZ6laX8izU").build()

    register_start(app)
    register_token_select(app)
    register_timeframe_select(app)
    register_analysis(app)

    app.run_polling()

if __name__ == '__main__':
    main()
