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

    def create_table_nasa_img(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS nasa_img(
                img_id SERIAL PRIMARY KEY,
                title VARCHAR (80),
                description TEXT,
                url TEXT,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        self.conn.commit()

    def create_table_p_in_space(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS p_in_space(
                id SERIAL PRIMARY KEY,
                num_of_people SMALLINT,
                name VARCHAR (120),
                role VARCHAR (80),
                last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        self.conn.commit()

    def save_p_in_space(self, num_of_people, name, role):
        self.cur.execute("""
            INSERT INTO p_in_space(num_of_people, name, role)
            VALUES (%s, %s, %s)""",(num_of_people, name, role))
        self.conn.commit()

    def get_p_space_from_db(self): #get data from db without scraping
        self.cur.execute("SELECT num_of_people, name, role, last_update FROM p_in_space;")
        data = self.cur.fetchall()
        if not data:
            return None
        n_of_ppl = data[0][0]
        people = {row[1]: row[2] for row in data}
        last_update = data[0][3]
        return n_of_ppl, people, last_update

    def save_img(self, title, description, url):
        self.cur.execute("SELECT img_id FROM nasa_img WHERE url = %s;", (url,))
        existing = self.cur.fetchone()
        if existing:
            return False # if the image is already in the db return true
        self.cur.execute("""
            INSERT INTO nasa_img(title, description, url)
            VALUES (%s, %s, %s)
            """, (title, description, url))
        self.conn.commit()
        return True

    def close(self):
        self.cur.close()
        self.conn.close()