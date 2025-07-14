from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import os
import json

# ---------- Load data ----------
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ---------- Keyboards ----------
main_keyboard = ReplyKeyboardMarkup(
    [["▶️ شروع", "⬅️ برگشت"], ["🔄 پاک کردن صفحه"]],
    resize_keyboard=True
)

def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("خطبه‌ها", callback_data="خطبه‌ها")],
        [InlineKeyboardButton("نامه‌ها", callback_data="نامه‌ها")],
        [InlineKeyboardButton("حکمت‌ها", callback_data="حکمت‌ها")]
    ])

# ---------- Handlers ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 سلام! یکی از دسته‌ها رو انتخاب کن:", reply_markup=get_main_menu())

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "▶️ شروع":
        await update.message.reply_text("📚 دسته موردنظر رو انتخاب کن:", reply_markup=get_main_menu())
    elif text == "⬅️ برگشت":
        await update.message.reply_text("🔙 برگشتی به منوی اصلی.", reply_markup=get_main_menu())
    elif text == "🔄 پاک کردن صفحه":
        await update.message.reply_text("✅ صفحه پاک شد.", reply_markup=main_keyboard)
    else:
        await update.message.reply_text("❓ لطفاً یکی از دکمه‌ها رو انتخاب کن.", reply_markup=main_keyboard)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice in data:
        buttons = [
            [InlineKeyboardButton(key, callback_data=f"{choice}|{key}")]
            for key in data[choice].keys()
        ]
        buttons.append([InlineKeyboardButton("⬅️ بازگشت", callback_data="بازگشت")])
        await query.edit_message_text(f"📂 {choice}:", reply_markup=InlineKeyboardMarkup(buttons))
    
    elif "|" in choice:
        cat, item = choice.split("|")
        text = data[cat][item]
        await query.edit_message_text(f"📖 {item}:\n\n{text}")
    
    elif choice == "بازگشت":
        await query.edit_message_text("📚 دسته موردنظر رو انتخاب کن:", reply_markup=get_main_menu())

# ---------- Run bot ----------
if __name__ == "__main__":
    token = os.environ.get("TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("✅ Bot is running...")
    app.run_polling()
