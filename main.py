import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv
import os
load_dotenv()
from handlers import image_of_day, start
from callbacks import Callback
from database import Database 

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
async def callback_query_router(update, context):
        handler = Callback(update, context)
        await handler.button_callback()
    

if __name__ == '__main__':
    db = Database()
    db.create_table()

    application = ApplicationBuilder().token(os.getenv("TELEGRAM_API")).build()
    
    start_handler = CommandHandler('start', start)
    img_of_day_handler = CommandHandler('Space_images', image_of_day)

    application.add_handler(start_handler)
    application.add_handler(img_of_day_handler)
    application.add_handler(CallbackQueryHandler(callback_query_router))


    application.run_polling()
    db.close()
    logging.info("db closed")
