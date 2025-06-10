from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler

async def start(update, context):
    keyboard = [["▶️ Mulai"], ["📥 Join Grup", "💬 Chat Customer Service"], ["❓ Help"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("✅ Selamat datang!", reply_markup=reply_markup)

def register_start(app):
    app.add_handler(CommandHandler("start", start))
