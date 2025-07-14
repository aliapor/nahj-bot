import telebot
from telebot import types
import json

TOKEN = "8037640720:AAGrKf2KH488zKE48FYAehCX_bBnIQie-AQ"
bot = telebot.TeleBot(TOKEN)

# داده‌ها
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# منوی اصلی
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📜 خطبه‌ها", callback_data="menu_khotbeh"),
        types.InlineKeyboardButton("📨 نامه‌ها", callback_data="menu_nameh"),
        types.InlineKeyboardButton("💎 حکمت‌ها", callback_data="menu_hekmat")
    )
    return markup

# دکمه بازگشت
def back_button():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_menu"))
    return markup

# شروع
@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = "🌟 به ربات نهج‌البلاغه خوش آمدی!\n\nیکی از گزینه‌های زیر رو انتخاب کن:"
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

# کلیک دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        bot.answer_callback_query(call.id)
        
        if call.data == "menu_khotbeh":
            markup = types.InlineKeyboardMarkup(row_width=1)
            for key in data["خطبه‌ها"]:
                markup.add(types.InlineKeyboardButton(key, callback_data=f"khotbeh_{key}"))
            markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="📜 لیست خطبه‌ها:", reply_markup=markup)

        elif call.data == "menu_nameh":
            markup = types.InlineKeyboardMarkup(row_width=1)
            for key in data["نامه‌ها"]:
                markup.add(types.InlineKeyboardButton(key, callback_data=f"nameh_{key}"))
            markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="📨 لیست نامه‌ها:", reply_markup=markup)

        elif call.data == "menu_hekmat":
            markup = types.InlineKeyboardMarkup(row_width=1)
            for key in data["حکمت‌ها"]:
                markup.add(types.InlineKeyboardButton(key, callback_data=f"hekmat_{key}"))
            markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="💎 لیست حکمت‌ها:", reply_markup=markup)

        elif call.data.startswith("khotbeh_"):
            key = call.data.replace("khotbeh_", "")
            text = f"{key}:\n\n{data['خطبه‌ها'][key]}"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=text, reply_markup=back_button())

        elif call.data.startswith("nameh_"):
            key = call.data.replace("nameh_", "")
            text = f"{key}:\n\n{data['نامه‌ها'][key]}"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=text, reply_markup=back_button())

        elif call.data.startswith("hekmat_"):
            key = call.data.replace("hekmat_", "")
            text = f"{key}:\n\n{data['حکمت‌ها'][key]}"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=text, reply_markup=back_button())

        elif call.data == "back_to_menu":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="🌟 برگشتی به منوی اصلی!\nیکی از گزینه‌ها رو انتخاب کن:", reply_markup=main_menu())

    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ خطا: {str(e)}")

# اجرا
if __name__ == "__main__":
    print("ربات راه افتاد!")
    bot.infinity_polling()
