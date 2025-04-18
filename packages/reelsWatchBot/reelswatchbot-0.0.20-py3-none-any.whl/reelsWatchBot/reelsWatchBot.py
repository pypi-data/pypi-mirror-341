from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import re
from instapy import Instapy

class ReelsWatchBot:
    def __init__(self, telegram_bot_token, turnstile, path="videos", url=r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"):
        if not telegram_bot_token:
            raise ValueError("Telegram bot token is required!")
        # This is an instance of the Instapy class from the instapy package that we will use to download the reels
        self.instapy = Instapy("", turnstile=turnstile)
        # Regex pattern that we will use to match URLs in messages 
        # (Default value matches any string that starts with http:// or https://)
        self.url = url
        # The Telegram bot token that we will use to authenticate with the Telegram API
        self.telegram_bot_token = telegram_bot_token
        # The path where the reels will be downloaded
        self.path = path

        self.turnstile = turnstile

        if turnstile == None:
            raise ValueError("Turnstile token is required!")

    
    # Function to start the bot
    async def start(update: Update, context):
        await update.message.reply_text('Send me a message with a link, and I will capture it!')

    # Function to handle messages with links
    async def handle_message(self, update: Update, context):
        message_text = update.message.text

        if ("set turnstile" in message_text):
            self.turnstile = message_text.split("set turnstile")[1].strip()
            self.instapy.set_turnstile(self.turnstile)
            await update.message.reply_text(f"Turnstile token set to: {self.turnstile}")
            return

        # Check if the message contains any URLs
        links = re.findall(self.url, message_text)

        if links:
            try:
                print(links)        
                # Download the reels from the links
                self.instapy.download_reels(reels_links=links, path=self.path)
                # Reply to the user with the number of links downloaded
                await update.message.reply_text(f"Thanks! Downloaded: {len(links)}")
            except Exception as e:
                # If there is an error downloading the links, log the error and reply to the user with an error message
                print(e)
                await update.message.reply_text(f"There was an error downloading one of the links you sent! Try again in a few minutes")
        else:
            # If no links are found in the message, reply to the user with a message
            await update.message.reply_text("No link found in the message.")
        
    def run_bot(self, start=None, handle_message=None):
        if start is None:
            start = self.start
        if handle_message is None:
            handle_message = self.handle_message

        print("Bot is running!")
        application = ApplicationBuilder().token(self.telegram_bot_token).build()
        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters=None, callback=handle_message))
        application.run_polling()