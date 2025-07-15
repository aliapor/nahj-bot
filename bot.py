import telebot
import json

# توکن بات
TOKEN = "8037640720:AAGrKf2KH488zKE48FYAehCX_bBnIQie-AQ"
bot = telebot.TeleBot(TOKEN)

# بارگذاری داده‌ها از فایل JSON
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# صفحه‌بندی
ITEMS_PER_PAGE = 20

# منوی اصلی
main_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.row("📜 خطبه‌ها", "📬 نامه‌ها", "💎 حکمت‌ها")

# دکمه بازگشت
back_button = telebot.types.InlineKeyboardMarkup()
back_button.add(telebot.types.InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_main"))

# شروع بات
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام! به ربات نهج‌البلاغه خوش اومدی 🌟\nیکی از گزینه‌های زیر رو انتخاب کن:", reply_markup=main_menu)

# انتخاب از منو
@bot.message_handler(func=lambda msg: msg.text in ["📜 خطبه‌ها", "📬 نامه‌ها", "💎 حکمت‌ها"])
def handle_menu(message):
    section = get_section_key(message.text)
    send_items_list(message.chat.id, section, page=1)

# ارسال لیست با صفحه‌بندی
def send_items_list(chat_id, section, page):
    items = list(data[section].items())
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    paginated = items[start:end]

    text = f"🗂 {section} (صفحه {page})\n\n"
    for key, _ in paginated:
        text += f"• {key}\n"

    keyboard = telebot.types.InlineKeyboardMarkup()
    for key, _ in paginated:
        keyboard.add(telebot.types.InlineKeyboardButton(key, callback_data=f"{section}:{key}"))

    nav = []
    if page > 1:
        nav.append(telebot.types.InlineKeyboardButton("⬅️ قبلی", callback_data=f"{section}_page_{page - 1}"))
    if end < len(items):
        nav.append(telebot.types.InlineKeyboardButton("➡️ بعدی", callback_data=f"{section}_page_{page + 1}"))
    if nav:
        keyboard.row(*nav)
    keyboard.add(telebot.types.InlineKeyboardButton("🏠 منوی اصلی", callback_data="back_to_main"))
    bot.send_message(chat_id, text, reply_markup=keyboard)

# کلیک روی دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "back_to_main":
        bot.send_message(call.message.chat.id, "بازگشت به منوی اصلی ☘️", reply_markup=main_menu)
    elif "_page_" in call.data:
        section, _, page = call.data.partition("_page_")
        send_items_list(call.message.chat.id, section, int(page))
    elif ":" in call.data:
        section, key = call.data.split(":")
        content = data[section][key]
        bot.send_message(call.message.chat.id, f"📖 {key}:\n\n{content}", reply_markup=back_button)

# نگاشت عنوان به کلید دیکشنری
def get_section_key(text):
    return {
        "📜 خطبه‌ها": "خطبه‌ها",
        "📬 نامه‌ها": "نامه‌ها",
        "💎 حکمت‌ها": "حکمت‌ها"
    }[text]

# اجرای ربات
print("🤖 ربات در حال اجراست...")
bot.infinity_polling()
