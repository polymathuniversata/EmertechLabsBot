from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters
from database import Database

# Define conversation states
(FIRST_NAME, LAST_NAME, AGE, COUNTRY, SKILLS, OCCUPATION, INTERESTS, 
 SHARE_KNOWLEDGE, CONTRIBUTE_MEETUPS) = range(9)

# Initialize database
db = Database()

async def start_registration(update: Update, context):
    await update.message.reply_text("Great! Let's start your registration. What's your first name?")
    return FIRST_NAME

async def process_first_name(update: Update, context):
    context.user_data['first_name'] = update.message.text
    await update.message.reply_text("What's your last name?")
    return LAST_NAME

async def process_last_name(update: Update, context):
    context.user_data['last_name'] = update.message.text
    await update.message.reply_text("What's your age?")
    return AGE

async def process_age(update: Update, context):
    try:
        age = int(update.message.text)
        context.user_data['age'] = age
        await update.message.reply_text("What's your permanent country of residence?")
        return COUNTRY
    except ValueError:
        await update.message.reply_text("Please enter a valid number for your age.")
        return AGE

async def process_country(update: Update, context):
    context.user_data['country'] = update.message.text
    await update.message.reply_text("What are your skills? (Separate multiple skills with commas)")
    return SKILLS

async def process_skills(update: Update, context):
    context.user_data['skills'] = update.message.text
    await update.message.reply_text("What's your occupation?")
    return OCCUPATION

async def process_occupation(update: Update, context):
    context.user_data['occupation'] = update.message.text
    await update.message.reply_text("What topics are you interested in learning? (Separate multiple topics with commas)")
    return INTERESTS

async def process_interests(update: Update, context):
    context.user_data['interests'] = update.message.text
    await update.message.reply_text("Are you willing to share knowledge with the community? (Yes/No)")
    return SHARE_KNOWLEDGE

async def process_share_knowledge(update: Update, context):
    context.user_data['share_knowledge'] = update.message.text.lower() == 'yes'
    await update.message.reply_text("Are you willing to contribute to support community meetups? (Yes/No)")
    return CONTRIBUTE_MEETUPS

async def process_contribute_meetups(update: Update, context):
    context.user_data['contribute_meetups'] = update.message.text.lower() == 'yes'
    context.user_data['user_id'] = update.effective_user.id
    
    # Save user data to the database
    db.add_user(context.user_data)
    
    await update.message.reply_text("Thank you for registering! Welcome to the Emertech Labs Community.")
    return ConversationHandler.END

async def cancel_registration(update: Update, context):
    await update.message.reply_text("Registration cancelled. You can start again anytime with /register.")
    return ConversationHandler.END

# Define the conversation handler
REGISTRATION_STEPS = {
    FIRST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_first_name)],
    LAST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_last_name)],
    AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_age)],
    COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_country)],
    SKILLS: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_skills)],
    OCCUPATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_occupation)],
    INTERESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_interests)],
    SHARE_KNOWLEDGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_share_knowledge)],
    CONTRIBUTE_MEETUPS: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_contribute_meetups)],
}
