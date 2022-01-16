"""Scrap functions
"""
import re

import requests
from bs4 import BeautifulSoup

# This value was defined on a local computer after some tests
# If better option are possible, do not hesitate to share it
DEFAULT_HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    "Accept-Language": "en-GB,en;q=0.5",
}

BING_IMG_URL = "https://www.bing.com/images/search?q="


class RequestException(Exception):
    pass


def create_header(url: str) -> dict:
    """Create a header dictionnary if it need
    to be changed (e.g. for an API)

    Parameters
    ----------
    url : str
        url to request (needed to get the host)

    Returns
    -------
    dict
        header dictionnary

    Raises
    ------
    TypeError
        url must be a string
    ValueError
        url must start with 'http'
    """
    if not isinstance(url, str):
        raise TypeError("url must be a string")
    if not (url.startswith("http://") or url.startswith("https://")):
        raise ValueError("url must start with 'http'")

    header = DEFAULT_HEADER

    url_split = url.split("//")
    http = url_split[0]
    host = url_split[1].split("/")[0]

    header["Host"] = host
    header["Referer"] = http + "//" + host
    header["Origin"] = http + "//" + host

    return header


def get_data_from_url(url: str) -> requests.Response:
    """Return answer of a request get
    from a wanted url

    Parameters
    ----------
    url : str
        url to request

    Returns
    -------
    requests.Response
        answer from requests.get function

    Raises
    ------
    TypeError
        url must be a string
    ValueError
        url must start with 'http'
    """

    if not isinstance(url, str):
        raise TypeError("url must be a string")
    if not (url.startswith("http://") or url.startswith("https://")):
        raise ValueError("url must start with 'http'")

    headers = create_header(url)
    r = requests.get(url, headers=headers)

    return r


def scrap_img_on_bing(keyword: str) -> list:
    """Scrap images on first page of Bing image page

    Parameters
    ----------
    keyword : str
        kerword for the research

    Returns
    -------
    list
        List of tuple (title, image url)

    Raises
    ------
    RequestException
        Request response is not valid
    """

    url = BING_IMG_URL + keyword
    ans = get_data_from_url(url)

    # if answer is not with a valid status
    if ans.status_code != 200:
        raise RequestException(
            "Request response is not valid (status code %s)" % ans.status_code
        )

    soup = BeautifulSoup(ans.text, "html.parser")
    images = soup.find_all("img")

    img_urls = []

    # regex for height and width on url
    regex = re.compile(r"&w=[0-9]*&h=[0-9]*", re.IGNORECASE)
    for item in images:

        # This attribute is the one to get image url with bing (last check jan 2022)
        if not item.has_attr("src2"):
            continue

        img_url = item.get("src2")
        # update image size to 200x200
        img_url = regex.sub("&w=200&h=200", img_url)
        img_ = (item.get("alt"), img_url)

        img_urls.append(img_)

    return img_urls


def get_img_url_list_from_keyword(keyword: str, engine="bing") -> list:
    """Retrieves images as list from a wanted engine.

    Currently only "bing" is available

    Parameters
    ----------
    keyword : str
        kerword for the research
    engine : str, optional
        engine to use, by default "bing"

    Returns
    -------
    list
        List of tuple (title, image url)

    Raises
    ------
    ValueError
        engine must be in ['bing']
    """

    if engine not in ["bing"]:
        raise ValueError("engine must be in ['bing']")

    if engine == "bing":
        img_list = scrap_img_on_bing(keyword)

    return img_list
