from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
load_dotenv()
from utils import fetch_apod_nasa_img, img_cache



async def image_of_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global img_cache
    await context.bot.send_message(chat_id=update.effective_chat.id, text="🤖​Bot is fetching something for you..")
    
    apod_img = fetch_apod_nasa_img() 

    keyboard = [[
        InlineKeyboardButton("What am i looking at❓", callback_data="explain"),
        InlineKeyboardButton("☄️​Next Image", callback_data="next"),
        InlineKeyboardButton("Save it!!💫​", callback_data="save")
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await update.message.reply_photo(photo=apod_img.url, caption=apod_img.title, reply_markup=reply_markup)
    
    except AttributeError: # if the button "Next image" is pressed
        await update.callback_query.message.reply_photo(photo=apod_img.url, caption=apod_img.title, reply_markup=reply_markup)

    except Exception as e:
        print("Error:", e)
        await context.bot.sendMessage(chat_id=update.effective_chat.id, text="Bot is at fault.. it is deeply sorry 💀​💀​")



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
            InlineKeyboardButton("Space images☄️", callback_data="space_images"),
            InlineKeyboardButton("What the bot can do 🪐​🚀​", callback_data="about"),
            InlineKeyboardButton("People in space 🌍", callback_data="p_in_space")
        ]]
    replay_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello and Welcome {update.effective_user.first_name}, ready to depart?🪐​")
    await context.bot.send_animation(chat_id=update.effective_chat.id, animation="https://media1.tenor.com/m/yqJrctJdvG0AAAAC/idk-khabib.gif", reply_markup=replay_markup)

   

    