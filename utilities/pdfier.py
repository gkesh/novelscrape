from urllib.error import URLError
from logging import error
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.print_page_options import PrintOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from base64 import b64decode
from os import path as opath, listdir


def pdfier(novel: str, source: str, pdfiy: str) -> None:
    outdir = f"/home/gkesh/Downloads/Novels/{novel}/"
    volumes_path = f"{source}/volumes/"

    if pdfiy == "all":
        volumes = listdir(volumes_path)
        for i in tqdm(range(len(volumes)), desc="Generating", ascii=False, ncols=100):
            volume = volumes[i]
            volume_name = volume[:volume.find(".")]
            if not pdf_print(outdir, f"{volume_name}.pdf", f"{volumes_path}{volume}"):
                break
        return

    pdf_print(outdir, f"{pdfiy}.pdf", f"{volumes_path}{pdfiy}.html")
    

def pdf_print(outdir: str, filename: str, path: str) -> bool:
    if not opath.exists(path):
        error(f"PDF print error. Path does not exist: {path}")
        return False 

    try:
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.set_preference("print.always_print_silent", True)
        options.set_preference("print.printer_Mozilla_Save_to_PDF.print_to_file", True)
        options.set_preference("print_printer", "Mozilla Save to PDF")
        
        browser = webdriver.Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))
        browser.get(f"file:///{path}")
        browser.set_page_load_timeout(5)

        print_options = PrintOptions()
        pdf_file = browser.print_page(print_options)
        
        with open(f"{outdir}/{filename}", "wb") as pdfw:
            pdfw.write(b64decode(pdf_file))

        browser.quit()
        return True
    except URLError:
        error(f"Failed to open file: {path}")
        return False