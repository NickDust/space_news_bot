import requests
from dotenv import load_dotenv
import os
from datetime import date, timedelta
load_dotenv()
from database import Database
from time import perf_counter


NASA_URL = "https://api.nasa.gov/"
"""
Take a random image from NASA APOD database.
"""
def fetch_apod_nasa_img():
    try:
        s = requests.Session()
        response = s.get(f"{NASA_URL}/planetary/apod", params={"api_key": os.getenv("NASA_API"), "count": 1}, timeout=3)
        data = response.json()[0]
        title = data.get("title")
        url = data.get("url")        
        explanation = data.get("explanation")
            
        return {"title": title, "url": url, "explanation": explanation}, False
    except Exception as e:
        db = Database()
        img = db.get_img_from_db()
        return img, True

def get_space_news():
    s = requests.Session()
    response = s.get("https://api.spaceflightnewsapi.net/v4/articles/?limit=5&offset=5&ordering=-published_at")
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
    s = requests.Session()
    try:
        response = s.get(f"{NASA_URL}/neo/rest/v1/feed?"
                                f"start_date={start_date}&end_date={end_date}&api_key={os.getenv("NASA_API")}")
        data = response.json()
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
    except Exception as e:
        return None

def get_quiz(difficulty):
    response = requests.get(f"https://opentdb.com/api.php?amount=10&category=17&difficulty={difficulty}&type=boolean")
    data = response.json()
    questions = []

    for q in data["results"]:
        questions.append({
            "question": q["question"],
            "correct": q["correct_answer"]
        })
    
    return questions