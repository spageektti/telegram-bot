from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from dotenv import load_dotenv
from os import getenv

from user import User
users = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello!")

    user = User(update.message.from_user.username, update.message.from_user.id)
    users.append(user)

def main():
    load_dotenv()

    application = Application.builder().token(getenv('TOKEN')).build()
    
    start_handler = CommandHandler("start", start)

    application.add_handler(start_handler)

    application.run_polling()

if __name__ == "__main__":
    main()