import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from icecream import ic
from random import randint
from selenium.webdriver.common.keys import Keys
import streamlit as st

"""
Scrap information from People Also Ask linked to the chosen entity.
By clicking on a PAA, other PAAs appear. These new PAAs form a new layer.
"""


def get_JV_features(entity):

    """
    Function that scrapes the People Also Ask from Google

    Args:
        entity: the entity to search on Google
        entity_type: the type of the entity
        sessions : research volume of the entity
        nb_layer : the number of PAA layer it will scrap

    Returns:
        list: a list of the scraped PAA
    """
    options = webdriver.ChromeOptions() 
    # options.add_argument("start-maximized")
    options.add_argument("headless")
    # options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_"+str(randint(0,15))+"_6) AppleWebKit/5"+str(randint(15,30))+".0 (KHTML, like Gecko) Chrome/"+str(randint(90,105))+".0.4290.88 Safari/5"+str(randint(30,40))+".0")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

    # url = "https://www.senscritique.com/search?filters%5B0%5D%5Bidentifier%5D=universe&filters%5B0%5D%5Bvalue%5D=Jeux&query=" + entity + "&size=16"
    # url = "https://www.senscritique.com/search?query=" + entity + "&size=16"
    # ic(url.replace(' ','%20'))
    # driver.get(url.replace(' ','%20'))
    driver.get("https://www.senscritique.com")
    driver.set_window_size(1920,1080)

    WebDriverWait(driver, 10)
    time.sleep(3)
    

    # driver.find_element(By.CSS_SELECTOR, 'span[class="didomi-continue-without-agreeing"]').click()

    WebDriverWait(driver, 10)
    time.sleep(3)
    driver.save_screenshot('screenshot.png')
    st.write(driver.current_url)
    st.image('screenshot.png')

    driver.find_element(By.CSS_SELECTOR, 'input[id="search"]').send_keys(entity)
    driver.find_element(By.CSS_SELECTOR, 'input[id="search"]').send_keys(Keys.RETURN)

    WebDriverWait(driver, 10)
    time.sleep(2)
    driver.save_screenshot('screenshot2.png')
    st.write(driver.current_url)
    st.image('screenshot2.png')

    driver.find_element(By.XPATH, '//a[text()="Jeux"]').click()

    WebDriverWait(driver, 10)
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, 'a[class="Text__SCText-sc-14ie3lm-0 Link__SecondaryLink-sc-1vfcbn2-1 jKqaHS jLGgsY"]').click()

    WebDriverWait(driver, 10)
    time.sleep(1)

    driver.get(driver.current_url + "/details")

    WebDriverWait(driver, 10)

    features = ""
    features_list = driver.find_element(By.CSS_SELECTOR, 'div[class="Text__SCText-sc-14ie3lm-0 Game__Text-sc-90jafw-1 ehXMwR iVrOIZ"]').text.split("\n")
    for el in features_list :
        if re.match(".+?(?= :)",el).group() in ["Éditeur","Éditeurs","Date de sortie (France)","Genre","Genres","PEGI"]:
            features += f"- {el}\n"

    return(features)

if __name__ == "__main__":
    ic(get_JV_features("fifa 23"))
