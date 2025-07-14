from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import json
import os

# Load data.json
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# دکمه‌های کیبورد پایین چت
main_keyboard = ReplyKeyboardMarkup(
    [["▶️ شروع", "⬅️ برگشت", "🔄 پاک کردن صفحه"]],
    resize_keyboard=True
)

# منوی اصلی دسته‌بندی‌ها
def main_menu():
    keyboard = [
        [InlineKeyboardButton("خطبه‌ها", callback_data="menu_خطبه‌ها")],
        [InlineKeyboardButton("نامه‌ها", callback_data="menu_نامه‌ها")],
        [InlineKeyboardButton("حکمت‌ها", callback_data="menu_حکمت‌ها")],
    ]
    return InlineKeyboardMarkup(keyboard)

# فهرست هر دسته
def submenu(category):
    keyboard = []
    for key in data.get(category, {}):
        keyboard.append([InlineKeyboardButton(key, callback_data=f"{category}::{key}")])
    keyboard.append([InlineKeyboardButton("⬅️ بازگشت", callback_data="بازگشت_به_منو")])
    return InlineKeyboardMarkup(keyboard)

# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌿 به ربات نهج‌البلاغه خوش آمدی!\nیکی از گزینه‌ها رو انتخاب کن:",
        reply_markup=main_keyboard
    )

# وقتی روی دکمه‌ها کلیک می‌شه
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data_callback = query.data

    if data_callback.startswith("menu_"):
        category = data_callback.split("_")[1]
        await query.edit_message_text(
            text=f"📚 فهرست {category}:",
            reply_markup=submenu(category)
        )
    elif "::" in data_callback:
        category, key = data_callback.split("::", 1)
        text = data.get(category, {}).get(key, "❌ محتوا یافت نشد.")
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ بازگشت", callback_data=f"menu_{category}")]]
        )
        await query.edit_message_text(text=text, reply_markup=keyboard)
    elif data_callback == "بازگشت_به_منو":
        await query.edit_message_text(
            text="🌿 لطفاً یکی از دسته‌ها رو انتخاب کن:",
            reply_markup=main_menu()
        )

# واکنش به پیام‌های متنی
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "▶️ شروع":
        await update.message.reply_text(
            "📖 یکی از دسته‌ها رو انتخاب کن:",
            reply_markup=main_menu()
        )
    elif text == "⬅️ برگشت":
        await update.message.reply_text(
            "🔙 برگشت به منوی اصلی:",
            reply_markup=main_menu()
        )
    elif text == "🔄 پاک کردن صفحه":
        await update.message.reply_text(
            "✅ صفحه پاک شد. دوباره از دکمه‌ها استفاده کن.",
            reply_markup=main_keyboard
        )
    else:
        await update.message.reply_text(
            "❓ لطفاً از دکمه‌ها استفاده کن.",
            reply_markup=main_keyboard
        )

# اجرای ربات
def main():
    token = os.getenv("TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("🤖 ربات فعال شد...")
    app.run_polling()

if __name__ == "__main__":
    main()
