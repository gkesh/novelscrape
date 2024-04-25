from itertools import chain
from multiprocessing import Pool
from tqdm import tqdm
from logging import info, error
from datetime import datetime
from time import sleep
from sys import exit
from argparse import ArgumentParser

from utilities.scrapper import scrape_chapter_list, scrape_chapter
from utilities.volumizer import compile_volumes, volumizer_filter

import json
import re

def multi_run(operation, links):
    with Pool(processes=12) as pool:
        return pool.map(operation, links)

def download_chapter(link: str) -> None:
    filename, content = scrape_chapter(link)

    if filename is None or content is None:
        error(f"Invalid filename or content for chapter link: {link}")
        return

    info(f"[{datetime.now()}] Downloading chapter: {filename}")

    with open(f"chapters/{filename}.md", "w") as w:
        w.write(content)


def fetch_config(novel: str) -> None:
    with open("config.json", "r") as config:
        return json.load(config)[novel]


def main(novel: str, volumize: str | None, start: int, end: int) -> None:
    config = fetch_config(novel)

    # Crawling chapter links
    chapter_list_template = f"{config['link']}/chapters?page=%d"
    chapters_links = list(chain.from_iterable(multi_run(scrape_chapter_list, [chapter_list_template % (page_no + 1) for page_no in range(start, end + 1)])))

    for i in tqdm(range(len(chapters_links)), desc="Downloading Chapters...", ascii=False, ncols=100):
        download_chapter(chapters_links[i])
        sleep(0.5)
    
    if volumize is not None:
        if "volumes" not in config:
            error(f"Volume config not available for {novel}, please update the config file!")
            return
        
        filter = volumizer_filter(volumize)
        volumizable_list = [volume for i, volume in enumerate(config["volumes"].items()) if filter(i + 1)]
        
        novel_base = f"novels/{novel}/"
        compile_volumes(f"{novel_base}/volumes", f"{novel_base}/chapters", volumizable_list)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("-n", "--novel", type=str, required=True)
    parser.add_argument("-v", "--volumize", type=str, required=False)
    parser.add_argument("-s", "--pstart", type=int, required=True)
    parser.add_argument("-e", "--pend", type=int, required=True)

    args = parser.parse_args()

    if args.volumize is not None and re.match("^[0-9]+(,[0-9]+)*$", args.volumize) is not None:
        error("Invalid value for volumize option, please enter comma seperated numbers without spaces!")
        exit(1)

    main(args.novel, args.volumize, args.pstart, args.pend)
