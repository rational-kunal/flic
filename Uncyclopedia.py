import requests
from bs4 import BeautifulSoup

MAIN_CONTENT_ID = "mw-content-text"
PREFIX_FOR_IMG = "https:"


class UncyclopediaResult:
    def __init__(self, summary, image_url_string):
        self.summary = summary
        self.image_url_string = image_url_string


class UncyclopediaManager:
    def fetch(self, uncyclopedia_url):
        page = requests.get(uncyclopedia_url)

        soup = BeautifulSoup(page.content, "html.parser")

        first_p = soup.find(id=MAIN_CONTENT_ID).find(name="p")

        img_url = None
        first_img = soup.find(name="img")
        if first_img and first_img.has_attr("src"):
            img_url = PREFIX_FOR_IMG + first_img.attrs["src"]

        # Remove "sup" and "sub"
        for tag in first_p.find_all(['sup', 'sub']):
            tag.decompose()

        return UncyclopediaResult(summary=first_p.text, image_url_string=img_url)


manager = UncyclopediaManager()
