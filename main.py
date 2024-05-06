from itertools import chain
from multiprocessing import Pool
from tqdm import tqdm
from logging import info, error
from datetime import datetime
from time import sleep
from sys import exit
from argparse import ArgumentParser, BooleanOptionalAction
from pathlib import Path

from utilities.scrapper import scrape_chapter_list, scrape_chapter
from utilities.volumizer import compile_volumes, volumizer_filter
from utilities.pdfier import pdfier

import json
import re
import os

def multi_run(operation, links):
    with Pool(processes=12) as pool:
        return pool.map(operation, links)


def initialize_novel(novel_path: str) -> None:
    # Creating novel paths
    Path(novel_path).mkdir(parents=True, exist_ok=True)
    Path(f"{novel_path}/chapters").mkdir(parents=True, exist_ok=True)
    Path(f"{novel_path}/volumes").mkdir(parents=True, exist_ok=True)


def download_chapter(novel: str, link: str) -> None:
    filename, content = scrape_chapter(link)

    if filename is None or content is None:
        error(f"Invalid filename or content for chapter link: {link}")
        return

    info(f"[{datetime.now()}] Downloading chapter: {filename}")

    with open(f"./novels/{novel}/chapters/{filename}.md", "w") as w:
        w.write(content)


def fetch_config(novel: str) -> None:
    with open("config.json", "r") as config:
        return json.load(config)[novel]


def main(novel: str, download: bool | None, volumize: str | None, start: int | None, end: int | None, pdfiy: bool | None) -> None:
    config = fetch_config(novel)

    # Setting novel base path
    novel_path = f"./novels/{novel}"

    # Checking if novel path exits
    if not Path(novel_path).exists():
        initialize_novel(novel_path)

    if download:
        # Crawling chapter links
        chapter_list_template = f"{config['link']}/chapters?page=%d"
        chapters_links = list(chain.from_iterable(multi_run(scrape_chapter_list, [chapter_list_template % (page_no) for page_no in range(start, end + 1)])))

        for i in tqdm(range(len(chapters_links)), desc="Downloading Chapters...", ascii=False, ncols=100):
            download_chapter(novel, chapters_links[i])
            sleep(1)

    if volumize is not None:
        if "volumes" not in config:
            error(f"Volume config not available for {novel}, please update the config file!")
            return
        
        filter = volumizer_filter(volumize)
        volumizable_list = [volume for i, volume in enumerate(config["volumes"].items()) if filter(i + 1)]
        
        compile_volumes(f"{novel_path}/volumes", f"{novel_path}/chapters", volumizable_list)
    
    if pdfiy is not None:
        pdfier(novel, os.path.abspath(novel_path), pdfiy)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("-n", "--novel", type=str, required=True)
    parser.add_argument("-v", "--volumize", type=str, required=False)
    parser.add_argument("-d", "--download", action=BooleanOptionalAction)
    parser.add_argument("-s", "--pstart", type=int, required=False)
    parser.add_argument("-e", "--pend", type=int, required=False)
    parser.add_argument("-p", "--pdfiy", type=str, required=False)

    args = parser.parse_args()

    if args.download and (args.pstart is None or args.pend is None):
        error("In download mode, please provide pstart and pend arguments as well!")
        exit(1)

    if args.volumize is not None and re.match("^[0-9]+(,[0-9]+)*$", args.volumize) is None:
        error("Invalid value for volumize option, please enter comma seperated numbers without spaces!")
        exit(1)

    main(
        args.novel, 
        args.download, 
        args.volumize, 
        args.pstart, 
        args.pend, 
        args.pdfiy
    )
