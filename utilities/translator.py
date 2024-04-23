from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from urllib.error import URLError
# from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import logging


def fetch(link: str) -> tuple[bool, any]:
    try:
        # page = urlopen(
        #     Request(
        #         link, 
        #         headers={'User-Agent': 'Mozilla/5.0'}
        #     )
        # ).read().decode('utf-8')
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        # executable_path param is not needed if you updated PATH
        browser = webdriver.Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))
        browser.get(link)
        page = browser.page_source

        el = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".reply-button"))).click()
        print(el)
        return True, page
    except URLError:
        logging.error(f"[ERROR] Invalid URL, Failed to fetch page: {link}")
        return False, None


def soup_factory(link: str) -> any:
    status, page = fetch(link)
    return BeautifulSoup(page, 'html.parser') if status else None

def scrape_translation(link: str) -> str:
    soup = soup_factory(link)

    if soup is None:
        logging.error(f"[ERROR] Returned empty page: {link}")
        return None

    return crawl_translation(soup)
    

def crawl_translation(soup) -> str:
    print(soup)
    translated: str = soup.find("span", {"class": "ryNqvb"}).text
    return translated

def main() -> None:
    trial = quote_plus("Hello you")
    source = f"https://translate.google.com/?sl=en&tl=sw&text={trial}&op=translate"

    print(scrape_translation(source))

if __name__ == "__main__":
    main()
