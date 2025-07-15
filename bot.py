import telebot
from telebot import types

bot = telebot.TeleBot("8037640720:AAGrKf2KH488zKE48FYAehCX_bBnIQie-AQ")

# -------------------- دستورات شروع --------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎬 شروع")
    bot.send_message(
        message.chat.id,
        "🎉 خوش‌اومدی به ربات نهج‌البلاغه!\n\n"
        "📚 اینجا می‌تونی خطبه‌ها، نامه‌ها و حکمت‌های امام علی علیه‌السلام رو به زبان فارسی بخونی.\n"
        "👇 برای شروع روی دکمه زیر بزن:",
        reply_markup=markup
    )

# -------------------- دکمه شروع --------------------
@bot.message_handler(func=lambda message: message.text == "🎬 شروع")
def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📜 خطبه‌ها", "📬 نامه‌ها")
    markup.row("💎 حکمت‌ها")
    bot.send_message(message.chat.id, "📖 لطفاً یکی از بخش‌های زیر رو انتخاب کن:", reply_markup=markup)

# -------------------- جای خالی برای اضافه‌کردن عملکرد هر بخش --------------------
@bot.message_handler(func=lambda message: message.text == "📜 خطبه‌ها")
def handle_khotbeh(message):
    bot.send_message(message.chat.id, "✅ بخش خطبه‌ها در حال آماده‌سازیه...")

@bot.message_handler(func=lambda message: message.text == "📬 نامه‌ها")
def handle_nama(message):
    bot.send_message(message.chat.id, "✅ بخش نامه‌ها به زودی میاد...")

@bot.message_handler(func=lambda message: message.text == "💎 حکمت‌ها")
def handle_hokmat(message):
    bot.send_message(message.chat.id, "✅ بخش حکمت‌ها به زودی راه‌اندازی می‌شه...")

# -------------------- اجرای ربات --------------------
bot.infinity_polling()
