import urllib.request

from bs4 import BeautifulSoup
from icecream import ic


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

def get_article(url):

    """
    Function that scrap a PurePeople article.

    Args:
        url (str): the url of the article.

    Returns:
        article (dict): a dictionary with all the necessary information
    """

    soup = get_html(url)

    main_text = ''
    for el in soup.find_all("div", {"class": "rich-text s-article"}) :
        main_text += el.text

    article = {
        "title": soup.find("div", {"id": "article-title"}).text,
        "summary": soup.find("div", {"class": "article__chapo u-padding-top--24px js-ga-insert-point"}).text,
        "main_text": main_text,
    }

    return article


if __name__ == "__main__":
    ic(get_article("https://www.purepeople.com/article/isabelle-adjani-retouchee-elle-repond-cash-oui-bien-sur-comme-toutes-les-actrices-francaises_a499728/1"))

