# handlers/start.py

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler

# State dari ConversationHandler
SELECTING_ACTION = 0

async def start(update, context):
    keyboard = [["▶️ Mulai"], ["📥 Join Grup", "💬 Chat Customer Service"], ["❓ Help"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("✅ Selamat datang!", reply_markup=reply_markup)
    return SELECTING_ACTION # Kembalikan state pertama

