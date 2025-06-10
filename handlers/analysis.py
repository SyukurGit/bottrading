import time
from telegram.ext import CallbackQueryHandler
from utils.cooldown import is_on_cooldown, update_cooldown
from utils.api_helper import get_token_data
from utils.ai_helper import analyze_token

async def start_analysis_callback(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    if is_on_cooldown(user_id):
        await query.answer("⚠️ Anda harus menunggu selama 3 menit untuk melanjutkan analisanya.", show_alert=True)
        return
    await query.answer()
    token = context.user_data.get('token')
    timeframe = context.user_data.get('timeframe')
    data = get_token_data(token, timeframe)
    result = analyze_token(token, timeframe, data)
    await query.message.reply_text(result)
    update_cooldown(user_id)

def register_analysis(app):
    app.add_handler(CallbackQueryHandler(start_analysis_callback, pattern="start_analysis"))
