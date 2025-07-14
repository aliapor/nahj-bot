import json
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = os.getenv('TOKEN')

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! خوش آمدید به ربات نهج‌البلاغه. /help را بفرستید.")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("/list - فهرست\n/get 1 - نمایش متن شماره 1")

def list_command(update: Update, context: CallbackContext):
    message = "فهرست مطالب:\n"
    for i, item in enumerate(data, 1):
        message += f"{i}. {item['type']} شماره {item['number']}\n"
    update.message.reply_text(message)

def get_command(update: Update, context: CallbackContext):
    args = context.args
    if not args or not args[0].isdigit():
        update.message.reply_text("لطفا شماره صحیح وارد کنید. مثلا: /get 2")
        return
    index = int(args[0]) - 1
    if index < 0 or index >= len(data):
        update.message.reply_text("شماره خارج از محدوده.")
        return
    item = data[index]
    update.message.reply_text(f"{item['type']} شماره {item['number']}:\n\n{item['translation']}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("list", list_command))
    dp.add_handler(CommandHandler("get", get_command))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
