import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from icecream import ic
from random import randint
from selenium.webdriver.common.keys import Keys

def get_JV_features(entity):

    """
    Function that scrap the features of a game on senscritic.

    Args:
        entity (str): the game you want to find.

    Returns:
        features (str): the features of the game chosen.
    """

    options = webdriver.ChromeOptions()
    # options.add_argument("start-maximized")
    options.add_argument("headless")
    # options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_"
        + str(randint(0, 15))
        + "_6) AppleWebKit/5"
        + str(randint(15, 30))
        + ".0 (KHTML, like Gecko) Chrome/"
        + str(randint(90, 105))
        + ".0.4290.88 Safari/5"
        + str(randint(30, 40))
        + ".0"
    )
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

    driver.get("https://www.senscritique.com")
    driver.set_window_size(1200, 800)

    WebDriverWait(driver, 10)
    time.sleep(3)

    driver.find_element(
        By.CSS_SELECTOR, 'span[class="didomi-continue-without-agreeing"]'
    ).click()

    WebDriverWait(driver, 10)

    driver.find_element(By.CSS_SELECTOR, 'input[id="search"]').send_keys(entity)
    driver.find_element(By.CSS_SELECTOR, 'input[id="search"]').send_keys(Keys.RETURN)

    WebDriverWait(driver, 10)
    time.sleep(2)

    driver.find_element(By.XPATH, '//a[text()="Jeux"]').click()

    WebDriverWait(driver, 10)
    time.sleep(2)

    driver.find_element(
        By.CSS_SELECTOR,
        'a[class="Text__SCText-sc-14ie3lm-0 Link__SecondaryLink-sc-1vfcbn2-1 jKqaHS jLGgsY"]',
    ).click()

    WebDriverWait(driver, 10)
    time.sleep(1)

    driver.get(driver.current_url + "/details")

    WebDriverWait(driver, 10)

    features = ""
    features_list = driver.find_element(
        By.CSS_SELECTOR,
        'div[class="Text__SCText-sc-14ie3lm-0 Game__Text-sc-90jafw-1 ehXMwR iVrOIZ"]',
    ).text.split("\n")
    for el in features_list:
        if re.match(".+?(?= :)", el).group() in [
            "Éditeur",
            "Éditeurs",
            "Date de sortie (France)",
            "Genre",
            "Genres",
            "PEGI",
        ]:
            features += f"- {el}\n"

    return features


if __name__ == "__main__":
    ic(get_JV_features("horizon forbidden west"))
