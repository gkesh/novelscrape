from bs4 import BeautifulSoup
from urllib.error import URLError
from urllib.request import Request, urlopen

from utilities.crawler import crawl_chapter_list, crawl_chapter

import logging


def fetch(link: str) -> tuple[bool, any]:
    try:
        page = urlopen(
            Request(
                link, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
        ).read().decode('utf-8')

        return True, page
    except URLError:
        logging.error(f"[ERROR] Invalid URL, Failed to fetch page: {link}")
        return False, None


def soup_factory(link: str) -> any:
    status, page = fetch(link)
    return BeautifulSoup(page, 'html.parser') if status else None


def scrape_chapter_list(link: str) -> list:
    soup = soup_factory(link)

    if soup is None:
        logging.error(f"[ERROR] Returned empty page: {link}")
        return None

    return crawl_chapter_list(soup)


def scrape_chapter(link: str) -> str:
    soup = soup_factory(link)

    if soup is None:
        logging.error(f"[ERROR] Returned empty page: {link}")
        return None

    return crawl_chapter(soup)
