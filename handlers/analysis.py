# handlers/analysis.py

import re
from telegram import ReplyKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram.constants import ParseMode
from telegram.error import BadRequest
from utils.cooldown import is_on_cooldown, update_cooldown
from utils.api_helper import get_binance_kline_data, get_funding_rate, get_long_short_ratio
from utils.ai_helper import get_professional_analysis
from utils.chart_helper import generate_candlestick_chart
import pandas as pd

def parse_analysis_for_levels(text: str) -> dict:
    levels = {}
    patterns = {
        'entry': r"Entry Price.*?\$\s*([\d,]+\.?\d*)",
        'sl': r"Stop Loss.*?\$\s*([\d,]+\.?\d*)",
        'tp1': r"Take Profit 1.*?\$\s*([\d,]+\.?\d*)",
        'tp2': r"Take Profit 2.*?\$\s*([\d,]+\.?\d*)",
        'tp3': r"Take Profit 3.*?\$\s*([\d,]+\.?\d*)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                price_str = match.group(1).replace(',', '')
                levels[key] = float(price_str)
            except (ValueError, IndexError):
                continue
    return levels

async def start_analysis_callback(update, context):
    query = update.callback_query
    await query.answer("Memproses analisis lengkap...")
    
    try:
        user_id = query.from_user.id
        if is_on_cooldown(user_id):
            await query.edit_message_text("⚠️ Anda harus menunggu cooldown selesai.")
            return

        token = context.user_data.get('token')
        timeframe_value = context.user_data.get('timeframe')
        timeframe_display_map = context.user_data.get('TIMEFRAMES', {})
        timeframe_display = [k for k, v in timeframe_display_map.items() if v == timeframe_value][0] or timeframe_value

        await query.edit_message_text(f"Mengambil data pasar untuk {token}...")
        kline_data = get_binance_kline_data(token, timeframe_value)
        if not kline_data:
            await query.edit_message_text(f"Gagal mendapatkan data candlestick dari Binance untuk {token}.")
            return
        funding_rate = get_funding_rate(token)
        long_short_ratio = get_long_short_ratio(token)

        clean_chart_image = generate_candlestick_chart(kline_data, token, timeframe_display)
        if clean_chart_image:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=clean_chart_image, caption=f"Chart Candlestick untuk {token.upper()}/USDT ({timeframe_display})")
        
        await context.bot.send_message(chat_id=query.message.chat_id, text="Membuat laporan analisis profesional...")
        text_analysis = get_professional_analysis(token, timeframe_display, kline_data, funding_rate, long_short_ratio)

        try:
            await context.bot.send_message(chat_id=query.message.chat_id, text=text_analysis, parse_mode=ParseMode.MARKDOWN)
        except BadRequest:
            await context.bot.send_message(chat_id=query.message.chat_id, text=text_analysis)

        price_levels = parse_analysis_for_levels(text_analysis)
        if price_levels:
            hlines_list, colors_list, styles_list = [], [], []
            level_map = {'entry': ('b', '--'), 'sl': ('r', '--'), 'tp1': ('g', ':'), 'tp2': ('g', ':'), 'tp3': ('g', ':')}
            for key, (color, style) in level_map.items():
                if key in price_levels:
                    hlines_list.append(price_levels[key])
                    colors_list.append(color)
                    styles_list.append(style)
            
            if hlines_list:
                # Menggunakan nama parameter yang benar: 'linestyle' (tanpa 's')
                hlines_data_for_chart = dict(hlines=hlines_list, colors=colors_list, linestyles=styles_list)
                
                annotated_chart_image = generate_candlestick_chart(
                    kline_data, 
                    token, 
                    timeframe_display, 
                    hlines_data=hlines_data_for_chart
                )
                
                if annotated_chart_image:
                    await context.bot.send_photo(chat_id=query.message.chat_id, photo=annotated_chart_image, caption="Chart dengan Anotasi Level Sinyal")

        update_cooldown(user_id)
        
        keyboard = [["Pilih Token Lain"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await context.bot.send_message(chat_id=query.message.chat_id, text="Analisis selesai.", reply_markup=reply_markup)

    except Exception as e:
        print(f"An error occurred in start_analysis_callback: {e}")
        await context.bot.send_message(chat_id=query.message.chat_id, text=f"Terjadi kesalahan tak terduga: {e}")