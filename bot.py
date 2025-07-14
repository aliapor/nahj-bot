import os
import json
import random
import logging
import telebot
from telebot import types

# --- Config ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load bot token from environment variables for security
try:
    TOKEN = os.environ["BOT_TOKEN"]
except KeyError:
    logging.error("BOT_TOKEN must be set in environment variables.")
    exit()

bot = telebot.TeleBot(TOKEN)

# --- Data Loading ---
try:
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    logging.info("Data loaded successfully.")
except (FileNotFoundError, json.JSONDecodeError) as e:
    logging.error(f"Could not load data.json: {e}")
    data = {"خطبه‌ها": {}, "نامه‌ها": {}, "حکمت‌ها": {}}

# --- Constants ---
ITEMS_PER_PAGE = 5

# --- Keyboards ---

def get_main_menu():
    """Creates the main menu keyboard."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📜 خطبه‌ها", callback_data="list_khotbeh_page_1"),
        types.InlineKeyboardButton("📨 نامه‌ها", callback_data="list_nameh_page_1"),
        types.InlineKeyboardButton("💎 حکمت‌ها", callback_data="list_hekmat_page_1"),
        types.InlineKeyboardButton("🎲 حکمت روز", callback_data="random_hekmat"),
        types.InlineKeyboardButton("🔎 جستجو", callback_data="search_start")
    )
    return markup

def create_paginated_keyboard(items_type, page):
    """Creates a paginated keyboard for lists."""
    markup = types.InlineKeyboardMarkup(row_width=1)
    items = list(data[items_type].keys())
    
    start_index = (page - 1) * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE
    
    # Add item buttons for the current page
    for key in items[start_index:end_index]:
        callback_prefix = items_type.rstrip('‌ها') # e.g., 'خطبه'
        markup.add(types.InlineKeyboardButton(key, callback_data=f"show_{callback_prefix}_{key}"))

    # Add navigation buttons
    nav_row = []
    if start_index > 0:
        nav_row.append(types.InlineKeyboardButton("◀️ قبلی", callback_data=f"list_{items_type}_page_{page-1}"))
    if end_index < len(items):
        nav_row.append(types.InlineKeyboardButton("بعدی ▶️", callback_data=f"list_{items_type}_page_{page+1}"))
    if nav_row:
        markup.row(*nav_row)
        
    markup.add(types.InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_menu"))
    return markup

def back_to_menu_button():
    """Creates a simple back to menu button."""
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_menu"))
    return markup

# --- Message Handlers ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Handles the /start command."""
    text = "🌟 به ربات نهج‌البلاغه خوش آمدید!\n\nمی‌توانید از گزینه‌های زیر برای مطالعه کلام امیرالمومنین (ع) استفاده کنید."
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

# --- Callback Query Handlers ---

@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    """Handles all callback queries from inline keyboards."""
    try:
        bot.answer_callback_query(call.id)
        
        # Main menu navigation
        if call.data == "back_to_menu":
            handle_back_to_menu(call)
        
        # Pagination lists
        elif call.data.startswith("list_"):
            handle_pagination(call)
            
        # Show content
        elif call.data.startswith("show_"):
            handle_show_content(call)
        
        # Special features
        elif call.data == "random_hekmat":
            handle_random_hekmat(call)
        elif call.data == "search_start":
            handle_search_start(call)

    except Exception as e:
        logging.error(f"Error in callback handler: {e}")
        bot.send_message(call.message.chat.id, "❌ یک خطای غیرمنتظره رخ داد. لطفا دوباره تلاش کنید.")

def handle_back_to_menu(call):
    """Edits the message to show the main menu."""
    text = "🌟 به منوی اصلی بازگشتید.\nیکی از گزینه‌ها را انتخاب کنید:"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=get_main_menu())

def handle_pagination(call):
    """Handles pagination for lists."""
    parts = call.data.split('_') # e.g., ['list', 'khotbeh', 'page', '1']
    items_type = parts[1]
    page = int(parts[3])
    
    markup = create_paginated_keyboard(items_type, page)
    bot.edit_message_text(f"📜 لیست {items_type}: (صفحه {page})", call.message.chat.id, call.message.message_id, reply_markup=markup)

def handle_show_content(call):
    """Shows the content of a selected item."""
    parts = call.data.split('_') # e.g., ['show', 'khotbeh', 'خطبه 1']
    item_type_singular = parts[1]
    item_key = "_".join(parts[2:])
    
    # Convert singular to plural for data access
    items_type_plural = item_type_singular + '‌ها'
    
    text = f"**{item_key}**\n\n{data[items_type_plural][item_key]}"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=back_to_menu_button(), parse_mode="Markdown")

def handle_random_hekmat(call):
    """Sends a random wisdom."""
    random_key, random_value = random.choice(list(data["حکمت‌ها"].items()))
    text = f"**🎲 حکمت روز: {random_key}**\n\n{random_value}"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=back_to_menu_button(), parse_mode="Markdown")

def handle_search_start(call):
    """Starts the search process."""
    msg = bot.send_message(call.message.chat.id, "لطفا کلمه یا عبارت مورد نظر خود را برای جستجو وارد کنید:")
    bot.register_next_step_handler(msg, process_search_query)

def process_search_query(message):
    """Processes the user's search query."""
    query = message.text.strip()
    if not query:
        bot.send_message(message.chat.id, "جستجو لغو شد. لطفا عبارتی را وارد کنید.", reply_markup=get_main_menu())
        return

    bot.send_message(message.chat.id, f"🔎 در حال جستجو برای «{query}»...")
    
    results = []
    for category, items in data.items():
        for key, value in items.items():
            if query in value or query in key:
                results.append(f"**در «{category} - {key}» یافت شد:**\n{value[:150]}...\n\n")

    if not results:
        bot.send_message(message.chat.id, f"هیچ نتیجه‌ای برای «{query}» یافت نشد.", reply_markup=back_to_menu_button())
        return

    response_text = f"**نتایج یافت‌شده برای «{query}»:**\n\n" + "".join(results)
    
    # Telegram has a message length limit of 4096 characters
    if len(response_text) > 4096:
        response_text = response_text[:4090] + "\n\n[...]"
        
    bot.send_message(message.chat.id, response_text, reply_markup=back_to_menu_button(), parse_mode="Markdown")


# --- Main Execution ---
if __name__ == "__main__":
    logging.info("Bot is starting...")
    bot.infinity_polling()

