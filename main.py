import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
import os
from dotenv import load_dotenv
from database import Database
from registration import start_registration, cancel_registration, REGISTRATION_STEPS

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database
db = Database()

async def start(update: Update, context):
    user = update.effective_user
    await update.message.reply_text(f"Welcome, {user.first_name}! I'm the Emertech Labs Community bot. "
                                    f"Use /register to join our community.")

async def welcome_new_member(update: Update, context):
    for new_member in update.message.new_chat_members:
        await update.message.reply_text(
            f"Welcome to Emertech Labs Community, {new_member.first_name}! "
            f"Please use /register to introduce yourself and join our community."
        )

def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    
    # Add the registration conversation handler
    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler('register', start_registration)],
        states=REGISTRATION_STEPS,
        fallbacks=[CommandHandler('cancel', cancel_registration)]
    ))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
