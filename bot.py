import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import json

# بارگذاری داده‌ها
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

TOKEN = os.getenv("TOKEN")

# ساخت لیست فهرست‌ها
categories = {
    "خطبه‌ها": list(data["خطبه‌ها"].keys()),
    "نامه‌ها": list(data["نامه‌ها"].keys()),
    "حکمت‌ها": list(data["حکمت‌ها"].keys())
}

keyboard = [["خطبه‌ها"], ["نامه‌ها"], ["حکمت‌ها"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "به ربات نهج‌البلاغه خوش آمدید.\nیکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if text in categories:
        items = categories[text]
        response = f"{text}:\n" + "\n".join(items[:30])  # فقط 30 مورد اول برای مثال
        await update.message.reply_text(response)
    
    else:
        # جستجو در تمام دسته‌ها
        for section in data:
            if text in data[section]:
                await update.message.reply_text(f"{text}:\n{data[section][text]}")
                return
        await update.message.reply_text("موردی یافت نشد!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.run_polling()
