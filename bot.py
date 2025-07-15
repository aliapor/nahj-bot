from telebot import TeleBot, types

bot = TeleBot('YOUR_TOKEN_HERE')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "🌟 *سلام به ربات نهج‌البلاغه خوش آمدی!* 🌟\n\n"\
                   "اینجا می‌تونی خطبه‌ها، نامه‌ها و حکمت‌های امام علی علیه‌السلام رو مطالعه کنی.\n"\
                   "👇 از منوی زیر انتخاب کن و شروع کن به خوندن! 📚"
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📜 خطبه‌ها", callback_data="khutbah"),
        types.InlineKeyboardButton("✉️ نامه‌ها", callback_data="nameh"),
        types.InlineKeyboardButton("💡 حکمت‌ها", callback_data="hekmat"),
        types.InlineKeyboardButton("🔙 بازگشت", callback_data="back")
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "khutbah":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="📜 *خطبه‌ها* را انتخاب کردی. کدوم خطبه رو می‌خوای؟\n(در حال آماده‌سازی...)",
                              parse_mode='Markdown')
        # اینجا کد صفحه‌بندی و ارسال خطبه‌ها میاد
    elif call.data == "nameh":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="✉️ *نامه‌ها* را انتخاب کردی. در حال بارگذاری...",
                              parse_mode='Markdown')
        # ارسال نامه‌ها
    elif call.data == "hekmat":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="💡 *حکمت‌ها* رو می‌بینی...",
                              parse_mode='Markdown')
        # ارسال حکمت‌ها
    elif call.data == "back":
        send_welcome(call.message)

bot.polling()
