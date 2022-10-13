import re
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

"""
Scrap information from People Also Ask linked to the chosen entity.
By clicking on a PAA, other PAAs appear. These new PAAs form a new layer.
"""


def get_PAA(entity, nb_layer=1):

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

    # op = webdriver.ChromeOptions()
    # op.add_argument("headless")
    driver = webdriver.Chrome()

    dict_list = []  # list to return
    nb_paa = 0
    rank = 1  # rank of the PAA, cumulative on the all entity
    elements = []  # list of the question related to their root question
    title_list = []  # list of the titles
    scrollElementIntoMiddle = (
        "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);"
        + "var elementTop = arguments[0].getBoundingClientRect().top;"
        + "window.scrollBy(0, elementTop-(viewPortHeight/2));"
    )

    driver.get(
        "https://www.google.com/search?hl=fr&q=" + str(entity)
    )  # hl=fr makes the research in French

    # link = driver.find_element(By.ID, "W0wltc")
    # link.click()  # to refuse google cookies

    WebDriverWait(driver, 10)

    if (
        driver.find_elements(
            By.CSS_SELECTOR, 'div[class="wQiwMc related-question-pair"]'
        )
        != []
    ):  # if the driver finds some PAAs
        paa = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'div[class="wQiwMc related-question-pair"]')
            )
        )
    else:
        driver.quit()
        return []

    for el in paa:
        if el.find_elements(By.CSS_SELECTOR, 'div[class="iDjcJe IX9Lgd wwB5gf"]') != []:
            elements.append(
                [
                    "",
                    el.find_element(
                        By.CSS_SELECTOR, 'div[class="iDjcJe IX9Lgd wwB5gf"]'
                    ).text,
                ]
            )

    for layer in range(nb_layer):

        paa = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'div[class="wQiwMc related-question-pair"]')
            )
        )

        nb_paa = len(paa)

        for i in range(rank - 1, nb_paa):  # to scrap just the new PAAs

            title = (
                paa[i]
                .find_element(By.CSS_SELECTOR, 'div[class="iDjcJe IX9Lgd wwB5gf"]')
                .text
            )

            if title not in title_list:
                title_list.append(title)

                if (
                    paa[i].find_elements(By.CSS_SELECTOR, 'span[class="hgKElc"]') != []
                ):  # to find the google answer to the PAA
                    answer = (
                        paa[i]
                        .find_element(By.CSS_SELECTOR, 'span[class="hgKElc"]')
                        .text
                    )
                else:
                    answer = ""

                if layer != nb_layer - 1:
                    driver.execute_script(scrollElementIntoMiddle, paa[i])
                    time.sleep(0.3)

                    paa[i].click()
                    time.sleep(1)

                    new_paa = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (
                                By.CSS_SELECTOR,
                                'div[class="wQiwMc related-question-pair"]',
                            )
                        )
                    )

                    for el in new_paa:
                        if el.find_elements(
                            By.CSS_SELECTOR, 'div[class="iDjcJe IX9Lgd wwB5gf"]'
                        ) != [] and el.find_element(
                            By.CSS_SELECTOR, 'div[class="iDjcJe IX9Lgd wwB5gf"]'
                        ).text not in [
                            row[1] for row in elements
                        ]:
                            elements.append(
                                [
                                    title,
                                    el.find_element(
                                        By.CSS_SELECTOR,
                                        'div[class="iDjcJe IX9Lgd wwB5gf"]',
                                    ).text,
                                ]
                            )  # append couples with the root question and the new ones

                for el in elements:
                    if title == el[1]:
                        root = el[0]

                if (
                    paa[i].find_elements(By.CSS_SELECTOR, 'div[class="yuRUbf"] > a')
                    != []
                ):
                    article = paa[i].find_element(
                        By.CSS_SELECTOR, 'div[class="yuRUbf"] > a'
                    )  # to find the article link to the PAA if it exists

                    url = article.get_attribute("href")
                    domain = re.search(
                        r"^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n?]+)",
                        article.get_attribute("href"),
                    ).group(0)
                else:

                    url = ""
                    domain = ""

                dict_list.append(
                    {
                        "title": title,
                        "url": url,
                        "domain": domain,
                        "layer": layer + 1,
                        "entity": entity,
                        "rank": rank,
                        "created_at": datetime.isoformat(datetime.now()),
                        "root": root,
                        "answer": answer,
                    }
                )

                rank += 1

    driver.quit()
    return dict_list


if __name__ == "__main__":
    print(get_PAA("saumon fumé", 1))
