from telegram.ext import Updater, MessageHandler, Filters
import requests
import os

TOKEN = 'YOUR_BOT_TOKEN'
DOODSTREAM_API_KEY = 'YOUR_DOODSTREAM_API_KEY'
DOODSTREAM_UPLOAD_URL = 'https://doodapi.com/api/upload/server?key={}'.format(DOODSTREAM_API_KEY)
DOODSTREAM_API_UPLOAD_URL = 'https://xxx.dood.video/upload/01?{}'.format(DOODSTREAM_API_KEY)

def start(update, context):
    update.message.reply_text('Welcome to your file upload bot!')

def handle_file(update, context):
    file_id = update.message.document.file_id
    file = context.bot.get_file(file_id)
    file_url = file.file_path

    # Download the file locally
    file_path = f'downloads/{file_id}.file'
    file.download(file_path)

    # Get DoodStream upload server
    response = requests.get(DOODSTREAM_UPLOAD_URL)
    server_info = response.json()

    if response.status_code == 200 and 'result' in server_info:
        server_url = server_info['result']

        # Upload the file to DoodStream
        with open(file_path, 'rb') as file_content:
            files = {'file': (os.path.basename(file_path), file_content)}
            payload = {'api_key': DOODSTREAM_API_KEY}
            doodstream_response = requests.post(server_url, files=files, data=payload)

            if doodstream_response.status_code == 200:
                doodstream_result = doodstream_response.json()
                if 'result' in doodstream_result:
                    download_url = doodstream_result['result'][0]['download_url']
                    update.message.reply_text(f'File uploaded successfully! Download link: {download_url}')
                else:
                    update.message.reply_text('Failed to get DoodStream result.')
            else:
                update.message.reply_text('Failed to upload file to DoodStream.')
    else:
        update.message.reply_text('Failed to get DoodStream upload server.')

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.document, handle_file))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_file))
    dp.add_handler(MessageHandler(Filters.command, start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
