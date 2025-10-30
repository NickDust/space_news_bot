from handlers import img_cache, image_of_day
import asyncio
from open_ai import Client
from database import Database
from scraper import people_in_space

class Callback:
    def __init__(self, update, context):
        self.update = update
        self.context = context
        self.query =  update.callback_query
        self.data = self.query.data

    async def button_callback(self):
        await self.query.answer()
        actions = {
            "explain": self.explain,
            "next": self.next,
            "save": self.save,
            "about": self.about,
            "space_images": self.space_images,
            "p_in_space": self.p_in_space
        }
        func = actions.get(self.query.data)
        if func:
            await func()

    async def explain(self): # Explain the picture with AI but if is not working take directly the nasa explanation
        await self.context.bot.sendMessage(chat_id=self.update.effective_chat.id, text="🤖​ Bot is thinking..")
        try:
            nasa_text = img_cache["explanation"]
            client = Client()
            explanation = client.img_analysis(nasa_text)
            print(explanation)
            await self.query.message.reply_text(explanation)
        except:
            await self.query.message.reply_text(nasa_text)
            
    async def next(self): # Take another random img
        await self.query.edit_message_reply_markup(reply_markup=None)
        message = self.query.message
        loading_message = await self.update.callback_query.message.reply_text("Loading.")
        for dots in ["Loading..", "Loading..."]:
            await asyncio.sleep(0.5)
            await loading_message.edit_text(dots)
        await loading_message.delete()
        await image_of_day(self.update, self.context)

    async def save(self): # Save img in Postgres database
        try:
            db = Database()
            await self.context.bot.sendMessage(chat_id=self.update.effective_chat.id, text="Saving in progress..💫​")
            saved = db.save_img(title=img_cache["title"], description=img_cache["explanation"], url=img_cache["url"])
            if saved:
                await self.context.bot.sendMessage(chat_id=self.update.effective_chat.id, text="✅​Image saved!💫​")
            else:
                await self.context.bot.sendMessage(chat_id=self.update.effective_chat.id, text="✔️Image already in the database!💫​")
        except Exception as e:
            print("Error saving image:", e)
            await self.context.bot.sendMessage(chat_id=self.update.effective_chat.id, text="❌​Failed to save image.💫​")

    async def about(self):
        await self.context.bot.send_message(chat_id=self.update.effective_chat.id, text="Im your Bot Austronat 🧑‍🚀​, I'am able to give you information and fun facts about space📡")

    async def space_images(self):
        await image_of_day(self.update, self.context)

    async def p_in_space(self):
        loading_message = await self.update.callback_query.message.reply_text("Loading.")
        for dots in ["Loading..", "Loading..."]:
            await asyncio.sleep(0.5)
            await loading_message.edit_text(dots)
        
        names, number = people_in_space()

        a_list = list(names.keys())
        a_names = [f".{name}" for name in a_list]
        text = "\n".join(a_names)
        
        await loading_message.delete()
        await self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=f"There are {number} people in space 🧑‍🚀​:\n {text} 📡")