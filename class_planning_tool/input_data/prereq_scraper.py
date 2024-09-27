from urllib import request
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup, ResultSet, Tag


def retrieve(url: str) -> str:
    resp = request.urlopen(request.Request(url, method="HEAD"), timeout=5)
    if resp.status != 200:
        raise HTTPError(url, resp.status, "Non-200 response received from request, could not retrieve prerequisites.")
    return resp.read()


def parse_prereq_block(block_content: str) -> list[list[str]]:
    """
    Parse prereq info from extras block content. Prereqs can be AND or OR situations and are all in one text string.

    Args:
        block_content (str): text from the appropriate block to parse
    
    Returns:
        list[list[str]]: prerequisite list. See get_prerequisites documentation for structure
    """
    pass


def extract_information(soup: BeautifulSoup) -> dict[str, list[list[str]]]:
    """
    Locate any instances of courseblock in the soup and construct a map of course codes to prerequisite course codes
    """

    course_blocks: ResultSet[Tag] = soup.find_all(name="div", class_="courseblock")
    for course_block in course_blocks:
        course_code: str = course_block.find("span", class_="detail-code").find("strong").get_text()
        course_title: str = course_block.find("span", class_="detail-title").find("strong").get_text()
        prereqs: list[list[str]] = []

        course_extras: ResultSet[Tag] = course_block.find_all("div", class_="courseblockextra")
        for extra in course_extras:
            block_strong = extra.find("strong")
            if not block_strong:
                continue
            if "prerequisite" not in block_strong.get_text().lower():
                continue

            prereqs.append(parse_prereq_block(extra.get_text()))


def get_prerequisites(url: str) -> dict[str, list[list[str]]]:
    """

    Args:
        url (str): URL of course information page
    
    Returns:
        dict[str, list[list[str]]] map of course codes to prerequisites. Prereqs are arranged as lists of lists, where
        the top level lists are prerequisite groups. Any course in the second-level list is sufficient to fulfill a prerequisite.
        For example, if CPSC5555 requires specifically CPSC1111 but also either of CPSC2222 or CPSC3333, the structure is:
        "CPSC5555": [
            ["CPSC1111"],
            ["CPSC2222", "CPSC3333"]
        ]
        A course with no prerequisites at all will have only an empty list, e.g.
        "CPSC5555": []
    
    Raises:
        ValueError if no URL is provided
        HTTPError or URLError (from retrieve function) if the webpage request fails


    """

    if not url:
        raise ValueError("Invalid URL or no URL provided.")
    
    content: str = retrieve(url)
    soup: BeautifulSoup = BeautifulSoup(content, "html.parser")

    return extract_information(soup)



