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
import undetected_chromedriver as uc

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

    # opts = webdriver.ChromeOptions()
    # opts.add_argument("headless")
    # opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_"+str(randint(0,15))+"_6) AppleWebKit/5"+str(randint(15,30))+".0 (KHTML, like Gecko) Chrome/"+str(randint(90,105))+".0.4290.88 Safari/5"+str(randint(30,40))+".0")
    # driver = webdriver.Chrome(options=op)


    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    # options.add_argument("headless")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options,executable_path='chromedriver.exe')
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    print(driver.execute_script("return navigator.userAgent;"))


    # driver = uc.Chrome(version_main=105)

    # time.sleep(uniform(2,4))
    # ic(driver.execute_script("return navigator.userAgent"))

    driver.get("https://www.micromania.fr/on/demandware.store/Sites-Micromania-Site/default/Search-Show?q= " + entity + " jeu")
    # driver.get("https://www.fnac.com/")
    # time.sleep(uniform(2,4))

    WebDriverWait(driver, 10)

    # driver.find_element(By.CSS_SELECTOR, 'input[type="search"]').send_keys(entity)
    # # driver.find_element(By.CSS_SELECTOR, 'input[id="Fnac_Search"]').send_keys(entity)
    # # time.sleep(uniform(2,4))
    # driver.find_element(By.CSS_SELECTOR, 'input[type="search"]').send_keys(Keys.RETURN)
    # # driver.find_element(By.CSS_SELECTOR, 'input[id="Fnac_Search"]').send_keys(Keys.RETURN)
    # # time.sleep(uniform(1,2))

    WebDriverWait(driver, 10)

    driver.find_element(By.CSS_SELECTOR, 'div[class="refinement-title-wrapper"]').click()

    time.sleep(3)

    driver.find_elements(By.CSS_SELECTOR, 'span[class="fake-checkbox"]')[1].click()

    time.sleep(3)

    driver.find_element(By.CSS_SELECTOR, 'button[class="trustarc-declineall-btn"]').click()

    time.sleep(0.3)

    driver.execute_script(scrollElementIntoMiddle, driver.find_element(By.CSS_SELECTOR, 'a[class="product-name-link pdp-link "]'))

    time.sleep(0.3)

    driver.find_element(By.CSS_SELECTOR, 'a[class="product-name-link pdp-link "]').click()

    time.sleep(300)

    WebDriverWait(driver, 10)

    features = driver.find_element(By.CSS_SELECTOR, 'table[class="table table-striped w-100"]').text

    # for row in driver.find_elements(By.CSS_SELECTOR, 'tr[class="table__row"]'):
    #     if row.find_elements(By.CSS_SELECTOR, 'th[class="table__cell"]') != []:
    #         if row.find_element(By.CSS_SELECTOR, 'th[class="table__cell"]').text in ['Date de sortie marché','Editeur','Genre du jeu vidéo','PEGI - Public']:
    #             if row.find_elements(By.CSS_SELECTOR, 'td[class="table__cell"]') != []:
    #                 features += f"""- {row.find_element(By.CSS_SELECTOR, 'th[class="table__cell"]').text} : {row.find_element(By.CSS_SELECTOR, 'td[class="table__cell"]').text}\n"""


    return(features)

if __name__ == "__main__":
    ic(get_JV("elden ring"))
