from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import requests
import os

TOKEN = 'YOUR_BOT_TOKEN'
DOODSTREAM_API_KEY = 'YOUR_DOODSTREAM_API_KEY'
# ... other constant declarations ...

def start(update, context):
    update.message.reply_text('Bot working!')

# ... existing code ...

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, handle_file))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_file))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
