import requests
from dotenv import load_dotenv
import os
from datetime import date, timedelta
load_dotenv()

img_cache = {}
NASA_URL = "https://api.nasa.gov/"
"""
Take a random image from NASA APOD database.
"""
def fetch_apod_nasa_img():
    global img_cache
    response = requests.get(f"{NASA_URL}planetary/apod", params={"api_key": os.getenv("NASA_API"), "count": 1}, timeout=10)
    data = response.json()[0]
    title = data.get("title")
    url = data.get("url")        
    explanation = data.get("explanation")
        
    img_cache["title"] = title
    img_cache["url"] = url,
    img_cache["explanation"] = explanation
    return {"title": title, "url": url, "explanation": explanation}

def get_space_news():
    response = requests.get("https://api.spaceflightnewsapi.net/v4/articles/?limit=5&offset=5&ordering=-published_at")
    data = response.json()

    articles = []
    for article in data["results"]:
        articles.append({
            "title": article["title"],
            "summary" : article["summary"],
            "url": article["url"],
            "image_url": article["image_url"]
            })
    return articles

def dangerous_asteroids():
    start_date = date.today().strftime("%Y-%m-%d")
    end_date = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
    response = requests.get(f"{NASA_URL}/neo/rest/v1/feed?"
                            f"start_date={start_date}&end_date={end_date}&api_key={os.getenv("NASA_API")}")
    data = response.json()
    print(data)
    results = []

    for day, asteroids in data["near_earth_objects"].items():
        for a in asteroids:
            if a["is_potentially_hazardous_asteroid"]:
                results.append({
                    "name": a["name"],
                    "day": day,
                    "distance_km": a["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"],
                    "approach_date": a["close_approach_data"][0]["close_approach_date_full"] 
                    })
    return results