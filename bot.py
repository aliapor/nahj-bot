import telebot
from telebot import types
import threading
import json

API_TOKEN = '8037640720:AAGrKf2KH488zKE48FYAehCX_bBnIQie-AQ'

bot = telebot.TeleBot(API_TOKEN)

lock = threading.Lock()

# بارگذاری داده‌ها از فایل JSON
with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

CACHE = {}  # کش ساده: key = (type, page), value = list of items

ITEMS_PER_PAGE = 20

def get_page_items(section, page):
    key = (section, page)
    if key in CACHE:
        return CACHE[key]
    items = list(data[section].items())
    start = (page -1)* ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_items = items[start:end]
    CACHE[key] = page_items
    return page_items

def generate_menu(section, page=1):
    markup = types.InlineKeyboardMarkup(row_width=1)
    page_items = get_page_items(section, page)
    for key, _ in page_items:
        btn = types.InlineKeyboardButton(key, callback_data=f"{section}:{key}")
        markup.add(btn)
    # دکمه صفحه قبل و بعد
    total_items = len(data[section])
    max_page = (total_items + ITEMS_PER_PAGE -1) // ITEMS_PER_PAGE
    nav_buttons = []
    if page >1:
        nav_buttons.append(types.InlineKeyboardButton('⬅️ قبلی', callback_data=f"{section}:page:{page-1}"))
    if page < max_page:
        nav_buttons.append(types.InlineKeyboardButton('بعدی ➡️', callback_data=f"{section}:page:{page+1}"))
    if nav_buttons:
        markup.row(*nav_buttons)
    # دکمه بازگشت
    markup.add(types.InlineKeyboardButton('🏠 بازگشت به منوی اصلی', callback_data='main_menu'))
    return markup

@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    with lock:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('📜 خطبه‌ها', callback_data='خطبه‌ها:page:1'))
        markup.add(types.InlineKeyboardButton('✉️ نامه‌ها', callback_data='نامه‌ها:page:1'))
        markup.add(types.InlineKeyboardButton('💡 حکمت‌ها', callback_data='حکمت‌ها:page:1'))
        bot.send_message(message.chat.id, "به ربات نهج‌البلاغه خوش آمدید. یکی از بخش‌ها را انتخاب کنید:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    with lock:
        data_call = call.data
        if data_call == 'main_menu':
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton('📜 خطبه‌ها', callback_data='خطبه‌ها:page:1'))
            markup.add(types.InlineKeyboardButton('✉️ نامه‌ها', callback_data='نامه‌ها:page:1'))
            markup.add(types.InlineKeyboardButton('💡 حکمت‌ها', callback_data='حکمت‌ها:page:1'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="به ربات نهج‌البلاغه خوش آمدید. یکی از بخش‌ها را انتخاب کنید:",
                                  reply_markup=markup)
            bot.answer_callback_query(call.id)
            return

        parts = data_call.split(':')
        if len(parts) == 3 and parts[1] == 'page':
            # تغییر صفحه
            section, _, page_str = parts
            page = int(page_str)
            markup = generate_menu(section, page)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"فهرست {section} - صفحه {page}",
                                  reply_markup=markup)
            bot.answer_callback_query(call.id)
            return

        elif len(parts) == 2:
            section, key = parts
            if section in data and key in data[section]:
                content = data[section][key]
                # دکمه بازگشت به فهرست بخش
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('⬅️ بازگشت', callback_data=f'{section}:page:1'))
                markup.add(types.InlineKeyboardButton('🏠 منوی اصلی', callback_data='main_menu'))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=content, reply_markup=markup)
                bot.answer_callback_query(call.id)
            else:
                bot.answer_callback_query(call.id, text='موردی یافت نشد.', show_alert=True)
            return
        else:
            bot.answer_callback_query(call.id, text='دستور نامعتبر است.', show_alert=True)

if __name__ == '__main__':
    print("ربات در حال اجراست...")
    bot.infinity_polling()
