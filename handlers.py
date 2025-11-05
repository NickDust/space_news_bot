from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
load_dotenv()
from utils import fetch_apod_nasa_img

user_progress = {}

async def image_of_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="🤖​Bot is fetching something for you..")
    
    apod_img = fetch_apod_nasa_img() 
    if apod_img == None:
        await context.bot.sendMessage(chat_id=update.effective_chat.id, text="Problems with NASA services.")
        return
    keyboard = [[
        InlineKeyboardButton("What am i looking at❓", callback_data="explain")],
        [InlineKeyboardButton("☄️​Next Image", callback_data="next"),
        InlineKeyboardButton("Save it!!💫​", callback_data="save")
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await update.message.reply_photo(photo=apod_img["url"], caption=apod_img["title"], reply_markup=reply_markup)
    
    except AttributeError: # if the button "Next image" is pressed
        await update.callback_query.message.reply_photo(photo=apod_img["url"], caption=apod_img["title"], reply_markup=reply_markup)

    except Exception as e:
        print("Error:", e)
        await context.bot.sendMessage(chat_id=update.effective_chat.id, text="Bot is at fault.. it is deeply sorry 💀​💀​")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
            InlineKeyboardButton("Space images☄️", callback_data="space_images"),
            InlineKeyboardButton("People in space 🌍", callback_data="p_in_space")],
            [InlineKeyboardButton("latest Space News 🌐", callback_data="news"),
             InlineKeyboardButton("Dangerous asteroids ☄️", callback_data="asteroids")],
             [InlineKeyboardButton("❓❔Super Quiz❓❔", callback_data="quiz")],
            [InlineKeyboardButton("What the bot can do 🪐​🚀​", callback_data="about"),
            
        ]]
    replay_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello and Welcome {update.effective_user.first_name}, ready to depart?🪐​")
    await context.bot.send_animation(chat_id=update.effective_chat.id, animation="https://media1.tenor.com/m/yqJrctJdvG0AAAAC/idk-khabib.gif", reply_markup=replay_markup)

async def trivia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("Easy 🍼​", callback_data="easy")],
        [InlineKeyboardButton("Medium 🤖​", callback_data="medium"),
        InlineKeyboardButton("Hard 👩‍🚀​", callback_data="hard")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text("Choose your difficulty!!", reply_markup=reply_markup)

async def poll_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.poll_answer
    user_id = answer.user.id
    selected_option = answer.option_ids[0]

    question_index = user_progress.get(user_id, 0)
    question_index += 1
    user_progress[user_id] = question_index

    if question_index < len(context.user_data["questions"][user_id]):
        next_q = context.user_data["questions"][user_id][question_index]
        await context.bot.send_poll(
            chat_id=answer.user.id,
            question=next_q["question"],
            options=["True", "False"],
            type='quiz',
            correct_option_id=["True", "False"].index(next_q["correct"]),
            is_anonymous=False,
        )
    else:
        await context.bot.send_message(
            chat_id=answer.user.id,
            text="✅ Quiz completed!"
        )