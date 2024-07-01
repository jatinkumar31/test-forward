import logging
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import os

# Configuration - Replace these with your actual values
BOT_TOKEN = '7180280603:AAG7eOiaGq995fQqm517iqDASd7p93L4ILI'
SOURCE_CHANNEL_USERNAME = '@sktechhub'  # Use the channel's username
TARGET_GROUP_ID = '-4251437575'  # Use the group ID

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def forward_message(update: Update, context: CallbackContext) -> None:
    message = update.channel_post
    if message and message.chat.username == SOURCE_CHANNEL_USERNAME.lstrip('@'):
        # Remove the specified text
        modified_text = message.text.replace("join our whatsapp channel now", "") if message.text else None

        if message.text:
            context.bot.send_message(chat_id=TARGET_GROUP_ID, text=modified_text, parse_mode=message.parse_mode)
        elif message.photo:
            context.bot.send_photo(chat_id=TARGET_GROUP_ID, photo=message.photo[-1].file_id, caption=modified_text, parse_mode=message.parse_mode)
        elif message.video:
            context.bot.send_video(chat_id=TARGET_GROUP_ID, video=message.video.file_id, caption=modified_text, parse_mode=message.parse_mode)
        # Handle other message types as needed

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.chat(username=SOURCE_CHANNEL_USERNAME.lstrip('@')), forward_message))

    updater.start_polling()

    # Start HTTP server to keep the service alive
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, BaseHTTPRequestHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    main()
