import re
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from random import randint, uniform
from icecream import ic
import undetected_chromedriver.v2 as uc

"""
Scrap information from People Also Ask linked to the chosen entity.
By clicking on a PAA, other PAAs appear. These new PAAs form a new layer.
"""


def get_JV(entity):

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

    scrollElementIntoMiddle = (
        "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);"
        + "var elementTop = arguments[0].getBoundingClientRect().top;"
        + "window.scrollBy(0, elementTop-(viewPortHeight/2));"
    )

    opts = webdriver.ChromeOptions()
    opts.add_argument("headless")
    # op.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_"+str(randint(0,15))+"_6) AppleWebKit/5"+str(randint(15,30))+".0 (KHTML, like Gecko) Chrome/"+str(randint(90,105))+".0.4290.88 Safari/5"+str(randint(30,40))+".0")
    # driver = webdriver.Chrome(options=op)
    driver = uc.Chrome(options=opts)

    # time.sleep(uniform(2,4))
    # ic(driver.execute_script("return navigator.userAgent"))

    driver.get("https://www.cdiscount.com/")
    # driver.get("https://www.fnac.com/")
    # time.sleep(uniform(2,4))

    WebDriverWait(driver, 10)

    driver.find_element(By.CSS_SELECTOR, 'input[type="search"]').send_keys(entity)
    # driver.find_element(By.CSS_SELECTOR, 'input[id="Fnac_Search"]').send_keys(entity)
    # time.sleep(uniform(2,4))
    driver.find_element(By.CSS_SELECTOR, 'input[type="search"]').send_keys(Keys.RETURN)
    # driver.find_element(By.CSS_SELECTOR, 'input[id="Fnac_Search"]').send_keys(Keys.RETURN)
    # time.sleep(uniform(1,2))

    WebDriverWait(driver, 10)

    driver.execute_script(scrollElementIntoMiddle, driver.find_element(By.CSS_SELECTOR, 'span[class="prdtTit"]'))

    time.sleep(0.3)

    driver.find_element(By.CSS_SELECTOR, 'span[class="prdtTit"]').click()

    WebDriverWait(driver, 10)

    features = ''

    for row in driver.find_elements(By.CSS_SELECTOR, 'tr[class="table__row"]'):
        if row.find_elements(By.CSS_SELECTOR, 'th[class="table__cell"]') != []:
            if row.find_element(By.CSS_SELECTOR, 'th[class="table__cell"]').text in ['Date de sortie marché','Editeur','Genre du jeu vidéo','PEGI - Public']:
                if row.find_elements(By.CSS_SELECTOR, 'td[class="table__cell"]') != []:
                    features += f"""- {row.find_element(By.CSS_SELECTOR, 'th[class="table__cell"]').text} : {row.find_element(By.CSS_SELECTOR, 'td[class="table__cell"]').text}\n"""


    return(features)

if __name__ == "__main__":
    ic(get_JV("elden ring"))
