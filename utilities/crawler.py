def crawl_chapter_list(soup) -> list:
    return [f"https://www.lightnovelpub.com{a['href']}" for a in soup.find("ul", {"class": "chapter-list"}).findAll("a", recursive = True)]


def crawl_chapter(soup) -> str:
    chapter_title: str = soup.find("span", {"class": "chapter-title"}).text
    chapter_content: str = "".join([f"<p>{p.string}</p>" for p in soup.find("div", {"id": "chapter-container"}).findAll("p", recursive = False)])
    
    file_title = chapter_title.replace(":", "").replace(" ", "_").replace("/", "_of_").lower()

    return file_title, f"<h3>{chapter_title}</h3><br>{chapter_content}"
