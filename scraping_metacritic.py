import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from random import randint
from icecream import ic

"""
Scrap information from People Also Ask linked to the chosen entity.
By clicking on a PAA, other PAAs appear. These new PAAs form a new layer.
"""


def get_JV_summary(entity):

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
    options.add_argument("headless")
    options.add_argument('--disable-dev-shm-usage')  
    # options.add_argument('--no-sandbox')
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_"+str(randint(0,15))+"_6) AppleWebKit/5"+str(randint(15,30))+".0 (KHTML, like Gecko) Chrome/"+str(randint(90,105))+".0.4290.88 Safari/5"+str(randint(30,40))+".0")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.metacritic.com/search/game/" + entity + "/results")

    WebDriverWait(driver, 10)
    time.sleep(2)

    # driver.find_element(By.CSS_SELECTOR, 'button[id="onetrust-reject-all-handler"]').click()

    WebDriverWait(driver, 10)

    el = driver.find_element(By.CSS_SELECTOR, 'h3[class="product_title basic_stat"]')
    el.find_element(By.CSS_SELECTOR, 'a').click()

    WebDriverWait(driver, 10)

    driver.find_element(By.CSS_SELECTOR, 'span[class="toggle_expand_collapse toggle_expand"]').click()

    WebDriverWait(driver, 10)

    summary = driver.find_element(By.CSS_SELECTOR, 'span[class="blurb blurb_expanded"]').text

    return(summary)

if __name__ == "__main__":
    ic(get_JV_summary("God of war"))
