from urllib import request
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup


def check_connection(url: str) -> bool:
    try:
        resp = request.urlopen(request.Request(url, method="HEAD"), timeout=5)
        if resp.status != 200:
            return False
    except HTTPError or URLError:
        return False
    return True

