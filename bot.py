import telebot
from telebot import types
import threading
import json

API_TOKEN = '8037640720:AAGrKf2KH488zKE48FYAehCX_bBnIQie-AQ'
bot = telebot.TeleBot(API_TOKEN)
lock = threading.Lock()

ITEMS_PER_PAGE = 20
CACHE = {}

# بارگذاری داده‌ها
with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

def get_page_items(section, page):
    key = (section, page)
    if key in CACHE:
        return CACHE[key]
    items = list(data[section].items())
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_items = items[start:end]
    CACHE[key] = page_items
    return page_items

def generate_menu(section, page=1):
    markup = types.InlineKeyboardMarkup(row_width=1)
    page_items = get_page_items(section, page)
    for key, _ in page_items:
        markup.add(types.InlineKeyboardButton(key, callback_data=f"{section}:{key}"))

    total_items = len(data[section])
    max_page = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    nav = []
    if page > 1:
        nav.append(types.InlineKeyboardButton("⬅️ قبلی", callback_data=f"{section}:page:{page-1}"))
    if page < max_page:
        nav.append(types.InlineKeyboardButton("بعدی ➡️", callback_data=f"{section}:page:{page+1}"))
    if nav:
        markup.row(*nav)

    markup.add(types.InlineKeyboardButton("🏠 بازگشت به منوی اصلی", callback_data="main_menu"))
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
    reply.add("🎬 شروع")
    bot.send_message(message.chat.id,
        "🎉 خوش اومدی به ربات نجات!\n\n"
        "📖 اینجا می‌تونی خطبه‌ها، نامه‌ها و حکمت‌های امام علی (ع) رو بخونی.",
        reply_markup=reply)

@bot.message_handler(func=lambda msg: msg.text == "🎬 شروع")
def start_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("📜 خطبه‌ها", callback_data="خطبه‌ها:page:1"))
    markup.add(types.InlineKeyboardButton("📬 نامه‌ها", callback_data="نامه‌ها:page:1"))
    markup.add(types.InlineKeyboardButton("💎 حکمت‌ها", callback_data="حکمت‌ها:page:1"))
    bot.send_message(message.chat.id, "یکی از بخش‌ها رو انتخاب کن:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    with lock:
        parts = call.data.split(':')

        if call.data == 'main_menu':
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("📜 خطبه‌ها", callback_data="خطبه‌ها:page:1"))
            markup.add(types.InlineKeyboardButton("📬 نامه‌ها", callback_data="نامه‌ها:page:1"))
            markup.add(types.InlineKeyboardButton("💎 حکمت‌ها", callback_data="حکمت‌ها:page:1"))
            bot.edit_message_text("یکی از بخش‌ها رو انتخاب کن:", call.message.chat.id, call.message.message_id, reply_markup=markup)
            bot.answer_callback_query(call.id)
            return

        if len(parts) == 3 and parts[1] == 'page':
            section, _, page_str = parts
            page = int(page_str)
            markup = generate_menu(section, page)
            bot.edit_message_text(f"📚 فهرست {section} - صفحه {page}", call.message.chat.id, call.message.message_id, reply_markup=markup)
            bot.answer_callback_query(call.id)
            return

        elif len(parts) == 2:
            section, key = parts
            if section in data and key in data[section]:
                content = data[section][key]
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("⬅️ بازگشت", callback_data=f"{section}:page:1"))
                markup.add(types.InlineKeyboardButton("🏠 منوی اصلی", callback_data="main_menu"))
                bot.edit_message_text(content, call.message.chat.id, call.message.message_id, reply_markup=markup)
                bot.answer_callback_query(call.id)
            else:
                bot.answer_callback_query(call.id, text="❌ موردی یافت نشد.", show_alert=True)
        else:
            bot.answer_callback_query(call.id, text="دستور نامعتبر.", show_alert=True)

print("🤖 ربات در حال اجراست...")
bot.infinity_polling()
