import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

class Database:
    def __init__(self):
        
        self.conn = psycopg2.connect(
                dbname="Telegram_bot",
                user= os.getenv("USER_DB"),
                password= os.getenv("PSW_DB"),
                host= os.getenv("HOST"))
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS nasa_img(
                img_id SERIAL PRIMARY KEY,
                title VARCHAR (80),
                description TEXT,
                url TEXT,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        self.conn.commit()

    def save_img(self, title, description, url):
        self.cur.execute("""
            INSERT INTO nasa_img(title, description, url)
            VALUES (%s, %s, %s)
            """, (title, description, url))
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()