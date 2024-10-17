from urllib import request
from urllib.error import HTTPError, URLError
from re import Pattern, compile

from bs4 import BeautifulSoup, ResultSet, Tag


COURSE_CODE_PATTERN: Pattern = compile(r"\b[A-Z]{4}\s*\d{4}[A-Z]?\b")

def retrieve(url: str) -> str:
    resp = request.urlopen(request.Request(url, method="GET"), timeout=5)
    if resp.status != 200:
        raise HTTPError(url, resp.status, "Non-200 response received from request, could not retrieve prerequisites.")
    return resp.read().decode("utf-8", "ignore").replace("\xa0", " ") # removes nbsp characters replace with regular spaces


def parse_prereq_block(block_content: str) -> list[list[str]]:
    """
    Parse prereq info from extras block content. Prereqs can be AND or OR situations and are all in one text string.

    Args:
        block_content (str): text from the appropriate block to parse
    
    Returns:
        list[list[str]]: prerequisite list. See get_prerequisites documentation for structure
    """
    results: list[list[str]] = []
    block_content = block_content.upper()
    prereq_groups: list[str] = block_content.split(" AND ")

    for group in prereq_groups:
        course_codes: list[str] = COURSE_CODE_PATTERN.findall(group)
        results.append(course_codes)
    return results
    


def extract_information(soup: BeautifulSoup) -> dict[str, list[list[str]]]:
    """
    Locate any instances of courseblock in the soup and construct a map of course codes to prerequisite course codes
    """
    results: dict[str, list[list[str]]] = {}

    course_blocks: ResultSet[Tag] = soup.find_all(name="div", class_="courseblock")
    for course_block in course_blocks:
        course_code: str = course_block.find("span", class_="detail-code").find("strong").get_text()
        #course_title: str = course_block.find("span", class_="detail-title").find("strong").get_text()
        prereqs: list[list[str]] = []

        course_extras: ResultSet[Tag] = course_block.find_all("div", class_="courseblockextra")
        for extra in course_extras:
            block_strong = extra.find("strong")
            if not block_strong:
                continue
            if "prerequisite" not in block_strong.get_text().lower():
                continue

            prereqs = parse_prereq_block(extra.get_text())
            break
        results[course_code] = prereqs
    return results


def get_prerequisites(url: str) -> dict[str, list[list[str]]]:
    """

    Args:
        url (str): URL of course information page
    
    Returns:
        dict[str, list[list[str]]] map of course codes to prerequisites. Prereqs are arranged as lists of lists, where
        the top level lists are prerequisite groups. Any course in the second-level list is sufficient to fulfill a prerequisite.
        For example, if CPSC 5555 requires specifically CPSC 1111 but also either of CPSC 2222 or CPSC 3333, the structure is:
        "CPSC 5555": [
            ["CPSC 1111"],
            ["CPSC 2222", "CPSC 3333"]
        ]
        A course with no prerequisites at all will have only an empty list, e.g.
        "CPSC 5555": []
    
    Raises:
        ValueError if no URL is provided
        HTTPError or URLError (from retrieve function) if the webpage request fails


    """

    if not url:
        raise ValueError("Invalid URL or no URL provided.")
    
    content: str = retrieve(url)
    soup: BeautifulSoup = BeautifulSoup(content, "html.parser")

    return extract_information(soup)



