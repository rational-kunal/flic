import logging
import requests
from bs4 import BeautifulSoup

MAIN_CONTENT_ID = "mw-content-text"
PREFIX_FOR_IMG = "https:"
FIRST_HEADING_ID = "firstHeading"


class UncyclopediaResult:
    def __init__(self, title, summary, main_image_url_string):
        self.title = title
        self.summary = summary
        self.main_image_url_string = main_image_url_string

    def __str__(self):
        return f"<UncyclopediaResult {self.title}>"


class UncyclopediaManager:
    def fetch(self, uncyclopedia_url):
        page = requests.get(uncyclopedia_url)

        soup = BeautifulSoup(page.content, "html.parser")

        title_el = soup.find(id=FIRST_HEADING_ID)

        first_p_el = soup.find(id=MAIN_CONTENT_ID).find(name="div", recursive=False, attrs={"class": "mw-parser-output"}).find(name="p", recursive=False)

        img_url_string = None
        first_img = soup.find(id=MAIN_CONTENT_ID).find(name="img")
        if first_img:
            if first_img.has_attr("srcset"):
                img_url_string = PREFIX_FOR_IMG + first_img.attrs["srcset"].split()[0]
            elif first_img.has_attr("src"):
                img_url_string = PREFIX_FOR_IMG + first_img.attrs["src"]

        # Remove "sup" and "sub"
        for tag in first_p_el.find_all(['sup', 'sub']):
            tag.decompose()

        result = UncyclopediaResult(title=title_el.text, summary=first_p_el.text,
                                    main_image_url_string=img_url_string)
        logging.info(f"Fetched {result}")
        return result


manager = UncyclopediaManager()

if __name__ == "__main__":
    result = manager.fetch("https://en.uncyclopedia.co/wiki/Special:RandomRootpage/Main")
    print(result)
