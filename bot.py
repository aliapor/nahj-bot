import telebot
from telebot import types
import json

TOKEN = "8037640720:AAGrKf2KH488zKE48FYAehCX_bBnIQie-AQ"

bot = telebot.TeleBot(TOKEN)

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📜 خطبه‌ها", callback_data="menu_khotbeh"),
        types.InlineKeyboardButton("📨 نامه‌ها", callback_data="menu_nameh"),
        types.InlineKeyboardButton("💎 حکمت‌ها", callback_data="menu_hekmat")
    )
    return markup

def back_button():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "به ربات نهج‌البلاغه خوش آمدید! لطفاً یکی از بخش‌ها را انتخاب کنید:", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id)
    
    if call.data == "menu_khotbeh":
        text = "خطبه‌ها:\n"
        for key in data["خطبه‌ها"]:
            text += f"- {key}\n"
        text += "\nبرای دیدن متن خطبه روی نام آن کلیک کنید."
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key in data["خطبه‌ها"]:
            markup.add(types.InlineKeyboardButton(key, callback_data=f"khotbeh_{key}"))
        markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu"))
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup)
        
    elif call.data == "menu_nameh":
        text = "نامه‌ها:\n"
        for key in data["نامه‌ها"]:
            text += f"- {key}\n"
        text += "\nبرای دیدن متن نامه روی نام آن کلیک کنید."
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key in data["نامه‌ها"]:
            markup.add(types.InlineKeyboardButton(key, callback_data=f"nameh_{key}"))
        markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu"))
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup)
        
    elif call.data == "menu_hekmat":
        text = "حکمت‌ها:\n"
        for key in data["حکمت‌ها"]:
            text += f"- {key}\n"
        text += "\nبرای دیدن متن حکمت روی نام آن کلیک کنید."
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key in data["حکمت‌ها"]:
            markup.add(types.InlineKeyboardButton(key, callback_data=f"hekmat_{key}"))
        markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_menu"))
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup)

    elif call.data.startswith("khotbeh_"):
        key = call.data.replace("khotbeh_", "")
        text = f"{key}:\n\n{data['خطبه‌ها'][key]}"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=back_button())
        
    elif call.data.startswith("nameh_"):
        key = call.data.replace("nameh_", "")
        text = f"{key}:\n\n{data['نامه‌ها'][key]}"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=back_button())
        
    elif call.data.startswith("hekmat_"):
        key = call.data.replace("hekmat_", "")
        text = f"{key}:\n\n{data['حکمت‌ها'][key]}"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=back_button())

    elif call.data == "back_to_menu":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="به منوی اصلی بازگشتید. لطفاً یکی از بخش‌ها را انتخاب کنید:", reply_markup=main_menu())

if __name__ == "__main__":
    print("Bot started!")
    bot.infinity_polling()
