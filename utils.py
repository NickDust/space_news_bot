import requests
from dotenv import load_dotenv
import os
from database import Database
load_dotenv()

img_cache = {}

"""
Take a random image from NASA APOD database.
"""
def fetch_apod_nasa_img():
    global img_cache
    response = requests.get("https://api.nasa.gov/planetary/apod", params={"api_key": os.getenv("NASA_API"), "count": 1}, timeout=10)
    data = response.json()[0]
    title = data.get("title")
    url = data.get("url")        
    explanation = data.get("explanation")
        
    img_cache["title"] = title
    img_cache["url"] = url,
    img_cache["explanation"] = explanation
    print(img_cache)
    return {"title": title, "url": url, "explanation": explanation}

