from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import requests
from dotenv import load_dotenv
import os
load_dotenv()

img_cache = {}

"""
Take a random image from NASA APOD database.
"""
async def image_of_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global img_cache
    await context.bot.send_message(chat_id=update.effective_chat.id, text="🤖​Bot is fetching something for you..")
    
    response = requests.get("https://api.nasa.gov/planetary/apod", params={"api_key": os.getenv("NASA_API"), "count": 1}, timeout=10)
    data = response.json()[0]
    title = data.get("title")
    url = data.get("url")        
    explanation = data.get("explanation")
        
    img_cache["title"] = title
    img_cache["url"] = url,
    img_cache["explanation"] = explanation

    keyboard = [[
        InlineKeyboardButton("What am i looking at❓", callback_data="explain"),
        InlineKeyboardButton("☄️​Next Image", callback_data="next"),
        InlineKeyboardButton("Save it!!💫​", callback_data="save")
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await update.message.reply_photo(photo=url, caption=title, reply_markup=reply_markup)
    
    except AttributeError: # if the button "Next image" is pressed
        await update.callback_query.message.reply_photo(photo=url, caption=title, reply_markup=reply_markup)

    except Exception as e:
        print("Error:", e)
        await context.bot.sendMessage(chat_id=update.effective_chat.id, text="Bot is at fault.. it is deeply sorry 💀​💀​")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
            InlineKeyboardButton("Space images☄️", callback_data="space_images"),
            InlineKeyboardButton("What i can do 🪐​🚀​", callback_data="about"),
        ]]
    replay_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello and Welcome {update.effective_user.first_name}, ready to depart?🪐​")
    await context.bot.send_animation(chat_id=update.effective_chat.id, animation="https://media1.tenor.com/m/yqJrctJdvG0AAAAC/idk-khabib.gif", reply_markup=replay_markup)

    

    