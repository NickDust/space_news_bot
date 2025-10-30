from bs4 import  BeautifulSoup
from selenium import webdriver
import time

def people_in_space(): 
    driver = webdriver.Chrome()
    driver.get("https://www.howmanypeopleareinspacerightnow.com/")

    time.sleep(3)
    peoples = {}
    soup = BeautifulSoup(driver.page_source, "html.parser")
    n_of_astrounats = soup.select_one("#container h1").text.strip()
    astrounats = soup.find_all(id="listing")

    
    for p in astrounats:
        names = p.find_all("div", class_="person-name")
        for name in names:
            tag = name.find("h2")
            role = name.find("h3")
            peoples[tag.text.strip()] = role.text.strip()
    driver.quit()
    return peoples, n_of_astrounats
    