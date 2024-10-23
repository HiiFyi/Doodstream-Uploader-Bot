from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import requests
import os

TOKEN = '7609207287:AAHNsu8KgFmicSN0aPIRcJe0DaeVeluV3hk'
DOODSTREAM_API_KEY = '462790fpirlczqa85lp0j4'
# ... other constant declarations ...

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='Bot working!')

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
