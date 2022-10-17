import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from icecream import ic

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
    options.add_argument("start-maximized")
    options.add_argument("headless")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options,executable_path='chromedriver.exe')
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    print(driver.execute_script("return navigator.userAgent;"))

    driver.get("https://www.senscritique.com/search?filters%5B0%5D%5Bidentifier%5D=universe&filters%5B0%5D%5Bvalue%5D=Jeux&query=" + entity + "&size=16")

    WebDriverWait(driver, 10)
    time.sleep(3)

    driver.find_element(By.CSS_SELECTOR, 'span[class="didomi-continue-without-agreeing"]').click()

    WebDriverWait(driver, 10)

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
