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
    print(url)
    request.add_header(
        "User-Agent",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    )
    try:
        raw_response = urllib.request.urlopen(request).read()
    except:
        print("waw")
        return None
    html = raw_response.decode("utf-8")

    return BeautifulSoup(html, "html.parser")


def get_JV(entity):

    """
    Function that scrap the phone number of an entity.

    Args:
        entity (str): the name of the entity.

    Returns:
        recipe (dict): a dictionary with the name of the entity and its phone number
    """
    url = "https://www.amazon.fr/s?k=" + entity + " jeu"

    soup = get_html(url.replace(" ", "+"))

    if soup.find("a", {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"}) is not None:
        print(soup.find("a", {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"}))
        new_url = soup.find("a", {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"}).attrs['href']
    
    soup = get_html("https://www.amazon.fr" + new_url)

    features = soup.find("div", {"id": "detailBullets_feature_div"}).text

    return features


if __name__ == "__main__":
    print(get_JV("FIFA 23"))
