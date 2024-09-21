from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import aiohttp

from dotenv import load_dotenv
from os import getenv

import random

from user import User
users = []

operators = ['+', '-', '*', '/']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! This bot is just to practice Python and Telegram API, so don't expect much from it.")

    user = User(update.message.from_user.username, update.message.from_user.id)

    for u in users:
        if u.id == user.id:
            return

    users.append(user)

async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = User(update.message.from_user.username, update.message.from_user.id)

    for u in users:
        if u.id == user.id:
            await update.message.reply_text(f"User {u.nickname} has {u.points} points.")
            return

    await update.message.reply_text("User not found.")

async def get_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("To get your points, solve this math question. For division, write number without decimal places (2 instead of 2.8).")
    
    number1 = random.randint(1, 10)
    number2 = random.randint(1, 10)

    operator = random.choice(operators)

    result = 0
    if operator == '+':
        result = number1 + number2
    elif operator == '-':
        result = number1 - number2
    elif operator == '*':
        result = number1 * number2
    elif operator == '/':
        result = number1 // number2  
    
    context.user_data['expected_answer'] = result
    context.user_data['user_id'] = update.message.from_user.id

    await update.message.reply_text(f"{number1} {operator} {number2} = ?")

async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = context.user_data.get('user_id')
    expected_answer = context.user_data.get('expected_answer')

    if update.message.from_user.id == user_id:
        try:
            user_answer = int(update.message.text)
            if user_answer == expected_answer:
                for u in users:
                    if u.id == user_id:
                        u.add_points(1)
                        await update.message.reply_text(f"Correct! You now have {u.points} points.")
                        return
            else:
                await update.message.reply_text("Incorrect!")
        except ValueError:
            await update.message.reply_text("Please enter a valid number.")

async def meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user = next((u for u in users if u.id == user_id), None)
    await update.message.reply_text("You want to spend one point to get a meme.")
    if user and user.points >= 1:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://meme-api.com/gimme') as response:
                if response.status == 200:
                    meme_data = await response.json()
                    meme_url = meme_data['url']
                    await update.message.reply_text(meme_url)
                    user.add_points(-1)
                    await update.message.reply_text(f"You have {user.points} points left.")
                else:
                    await update.message.reply_text("Failed to fetch meme. Please try again later.")
    else:
        await update.message.reply_text("You don't have enough points to get a meme.")

def main():
    load_dotenv()

    application = Application.builder().token(getenv('TOKEN')).build()
    
    start_handler = CommandHandler("start", start)
    points_handler = CommandHandler("points", points)
    get_points_handler = CommandHandler("get_points", get_points)
    answer_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer)
    meme_handler = CommandHandler("meme", meme)

    application.add_handler(start_handler)
    application.add_handler(points_handler)
    application.add_handler(get_points_handler)
    application.add_handler(answer_handler)
    application.add_handler(meme_handler)

    application.run_polling()

if __name__ == "__main__":
    main()
