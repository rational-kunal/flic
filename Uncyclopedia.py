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


class UncyclopediaManager:
    def fetch(self, uncyclopedia_url):
        page = requests.get(uncyclopedia_url)

        soup = BeautifulSoup(page.content, "html.parser")

        title_el = soup.find(id=FIRST_HEADING_ID)

        first_p_el = soup.find(id=MAIN_CONTENT_ID).find(name="p")

        img_url_string = None
        first_img = soup.find(id=MAIN_CONTENT_ID).find(name="img")
        if first_img and first_img.has_attr("srcset"):
            img_url_string = PREFIX_FOR_IMG + first_img.attrs["srcset"].split()[0]

        # Remove "sup" and "sub"
        for tag in first_p_el.find_all(['sup', 'sub']):
            tag.decompose()

        return UncyclopediaResult(title=title_el.text, summary=first_p_el.text,
                                  main_image_url_string=img_url_string)


manager = UncyclopediaManager()
