from bs4 import  BeautifulSoup
from selenium import webdriver
import time
from database import Database

def people_in_space(): 
    driver = webdriver.Chrome()
    driver.get("https://www.howmanypeopleareinspacerightnow.com/")

    time.sleep(3)
    people = {}
    soup = BeautifulSoup(driver.page_source, "html.parser")
    n_of_astrounats = soup.select_one("#container h1").text.strip()
    astrounats = soup.find_all(id="listing")
    
    for p in astrounats:
        names = p.find_all("div", class_="person-name")
        for name in names:
            tag = name.find("h2")
            role = name.find("h3")
            people[tag.text.strip()] = role.text.strip()
    db = Database()
    db.create_table_p_in_space()
    for name, role in people.items():
        db.save_p_in_space(num_of_people=int(n_of_astrounats), name=name, role=role)
    driver.quit()
    return people, n_of_astrounats
    