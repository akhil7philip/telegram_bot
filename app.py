import os
import logging
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PollAnswerHandler,
    PollHandler,
    filters,
)
from dotenv import load_dotenv
import lang_rules
from constants import Language

load_dotenv()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Replace 'YOUR_TOKEN' with your actual bot token
TOKEN = os.getenv('TELEGRAM_TOKEN')

bn = Language.bn.value
en = Language.en.value
default_lang = bn
print(f"default_lang: {default_lang}")

def get_intro(lang: str) -> str:
    return {
        en: lang_rules.english_intro,
        bn: lang_rules.bangla_intro,
    }.get(lang)

def get_options(lang: str) -> str:
    return {
        en: [[option] for option in lang_rules.english_rules.keys()],
        bn: [[option] for option in lang_rules.bangla_rules.keys()],
    }.get(lang)

def get_response(option: str, lang: str) -> str:
    return {
        en: lang_rules.english_rules.get(option),
        bn: lang_rules.bangla_rules.get(option)
    }.get(lang)

def get_final_options(lang: str) -> str:
    return {
        en: [[option] for option in lang_rules.english_end],
        bn: [[option] for option in lang_rules.bangla_end],
    }.get(lang)
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Inform user about what this bot can do"""
    await update.message.reply_text(
        """ডিএল এবং এলআরও বটে স্বাগতম! আপনার ভাষা চয়ন করুন:
        Welcome to the DL&LRO Bot! Please enter language:""",
        reply_markup={
        "keyboard": [
            [bn, en]
        ],
        "one_time_keyboard": True,
        "resize_keyboard": True})
    
async def choose_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global default_lang
    default_lang = update.message.text
    logging.info(f"lang_choice: {default_lang}")
    logging.info(f"get_options: {get_options(default_lang)}")
    await update.message.reply_text(
        get_intro(default_lang),
        reply_markup={
        "keyboard": get_options(default_lang),
        "one_time_keyboard": True,
        "resize_keyboard": True})

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global default_lang
    user_choice = update.message.text
    logging.info(f"user_choice: {user_choice}")
    await update.message.reply_text(
        get_response(user_choice, default_lang),
        reply_markup={
        "keyboard": get_final_options(default_lang),
        "one_time_keyboard": True,
        "resize_keyboard": True})
    start(update, None)

def main() -> None:
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, choose_options))
    app.add_handler(MessageHandler(filters.TEXT, handle_choice))
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
