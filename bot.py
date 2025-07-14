from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# داده نمونه (همون data.json به شکل دیکشنری)
data = {
    "خطبه‌ها": {
        "خطبه 1": "سپاس خدایی را سزاست که آفرینش را آغاز کرد...",
        "خطبه 2": "خداوند را سپاس می‌گویم که ما را به راه هدایت نمود...",
        "خطبه 3": "ای مردم، تقوا پیشه کنید و از خدا بترسید..."
    },
    "نامه‌ها": {
        "نامه 1": "از علی بن ابی‌طالب به مالک اشتر...",
        "نامه 2": "نامه به معاویه که در آن او را از دشمنی نهی می‌کند...",
        "نامه 3": "نامه‌ای به عبدالله بن عباس که او را به تقوا فرا می‌خواند..."
    },
    "حکمت‌ها": {
        "حکمت 1": "ارزش هر کس به اندازه کاری است که آن را نیکو انجام می‌دهد.",
        "حکمت 2": "سکوت، پوششی برای نادانی و زینتی برای دانا است.",
        "حکمت 3": "کسی که نفس خود را بشناسد، پروردگارش را شناخته است."
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("خطبه‌ها", callback_data='خطبه‌ها')],
        [InlineKeyboardButton("نامه‌ها", callback_data='نامه‌ها')],
        [InlineKeyboardButton("حکمت‌ها", callback_data='حکمت‌ها')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📚 لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data
    
    if category in data:
        keyboard = []
        for key in data[category].keys():
            keyboard.append([InlineKeyboardButton(key, callback_data=f"{category}|{key}")])
        keyboard.append([InlineKeyboardButton("بازگشت", callback_data="بازگشت")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"✅ {category} مورد نظر را انتخاب کنید:", reply_markup=reply_markup)
    
    elif '|' in category:
        cat, item = category.split('|')
        text = data.get(cat, {}).get(item, "متاسفانه اطلاعاتی یافت نشد.")
        await query.edit_message_text(f"📖 {item}:\n\n{text}")
    
    elif category == "بازگشت":
        await query.edit_message_text(
            "📚 لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("خطبه‌ها", callback_data='خطبه‌ها')],
                [InlineKeyboardButton("نامه‌ها", callback_data='نامه‌ها')],
                [InlineKeyboardButton("حکمت‌ها", callback_data='حکمت‌ها')]
            ])
        )

if __name__ == '__main__':
    import os
    token = os.environ.get('TOKEN')  # توکن رو باید تو محیط متغیر بگذاری
    
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot started...")
    app.run_polling()
