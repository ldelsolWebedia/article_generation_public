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

def p_or_ul_has_no_class(tag) :
     return tag.name in ["p","ul"] and not tag.has_attr('class')

def p_has_no_class(tag) :
     return tag.name == "p" and not tag.has_attr('class')

def get_article(url,site):

    """
    Function that scrap a PurePeople article.

    Args:
        url (str): the url of the article.

    Returns:
        article (dict): a dictionary with all the necessary information
    """

    soup = get_html(url)

    paragraphe_list = []

    # if site in ["GameStar","3DJuegos"] and soup.find_all("div", {"class": "article-content"}) != []:
    #     return(soup.find("div", {"class": "article-content"}).text)
    
    if site == "Mein-MMO" and soup.find_all("div", {"class": "gp-entry-content"}) != []:
        article_content = soup.find("div", {"class": "gp-entry-content"})
        for el in article_content.find_all(p_or_ul_has_no_class) :
            paragraphe_list.append(el.text)
        return(paragraphe_list)

    if site in ["GameStar","3DJuegos"] and soup.find_all("div", {"class": "article-content"}) != []:
        article_content = soup.find("div", {"class": "article-content"})
        for el in article_content.find_all(p_or_ul_has_no_class) :
            paragraphe_list.append(el.text)
        return(paragraphe_list)
    
    if site in ["Espinof"] and soup.find_all("div", {"class": "blob js-post-images-container"}) != []:
        article_content = soup.find("div", {"class": "blob js-post-images-container"})
        for el in article_content.find_all(p_or_ul_has_no_class) :
            paragraphe_list.append(el.text)
        return(paragraphe_list)
    
    if site in ["MOVIEPILOT NEWS"] and soup.find_all("div", {"class": "sc-gsDKAQ sc-czc4w4-0 fPGaEA iXAenB"}) != []:
        article_content = soup.find("div", {"class": "sc-gsDKAQ sc-czc4w4-0 fPGaEA iXAenB"})
        for el in article_content.find_all(p_has_no_class) :
            paragraphe_list.append(el.text)
        return(paragraphe_list)
    
    if site in ["SensaCine"] and soup.find_all("div", {"class": "article-content"}) != []:
        article_content = soup.find("div", {"class": "article-content"})
        for el in article_content.find_all("p", {"class": "bo-p"}) :
            paragraphe_list.append(el.text)
        return(paragraphe_list)

    return("Error in the scraping process")


if __name__ == "__main__":
    ic(get_article("https://www.moviepilot.de/news/neues-netflix-meisterwerk-1899-ist-gruseliger-als-dark-und-bringt-euer-hirn-zum-platzen-1138932","MOVIEPILOT NEWS"))

