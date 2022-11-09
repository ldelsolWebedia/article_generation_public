import urllib.request

from bs4 import BeautifulSoup


def get_html(url):

    """
    Function that get the html code from a given url.

    Args:
        url (str): the url to get html code from.

    Returns:
        str: the html code from the given url.
    """

    request = urllib.request.Request(url)
    request.add_header(
        "User-Agent",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    )
    try:
        raw_response = urllib.request.urlopen(request).read()
    except:
        return None
    html = raw_response.decode("utf-8")

    return BeautifulSoup(html, "html.parser")


def find_all_entities(soup, html_type, entity):
    result = []
    if soup.find_all(html_type, entity) is not None:
        for el in soup.find_all(html_type, entity):
            result.append(el.text)
    return result


def get_recipe(url):

    """
    Function that scrap a 750g recipe.

    Args:
        url (str): the url of the recipe.

    Returns:
        recipe (dict): a dictionary with all the necessary information
    """

    soup = get_html(url)

    if soup.find("span", {"class": "u-title-page u-align-center"}) is not None:
        title = soup.find("span", {"class": "u-title-page u-align-center"}).text

    recipe = {
        "title": title,
        "ingredients": find_all_entities(
            soup, "li", {"class": "is-6 recipe-ingredients-item"}
        ),
        "features": find_all_entities(soup, "div", {"class": "recipe-info-item"}),
        "equipments": find_all_entities(
            soup, "span", {"class": "recipe-equipments-item-label"}
        ),
        "steps": find_all_entities(soup, "div", {"class": "recipe-steps-text"}),
        "nutrition": find_all_entities(soup, "div", {"class": "u-iblock"}),
    }

    return recipe


if __name__ == "__main__":
    print(get_recipe("https://www.750g.com/cookies-aux-pepites-de-chocolat-r89377.htm"))
