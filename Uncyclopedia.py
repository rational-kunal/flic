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

        if "UnNews" in uncyclopedia_url:
            return self.transfromUnNews(soup)

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

    def transfromUnNews(self, soup: BeautifulSoup) -> UncyclopediaResult:
        heading = soup.find(name="span", attrs={"class": "mw-page-title-main"}).text

        container = soup.find(name="div", attrs={"class": "mw-parser-output"})

        img_url_string = None
        first_img = container.find(name="img")
        if first_img:
            if first_img.has_attr("srcset"):
                img_url_string = PREFIX_FOR_IMG + first_img.attrs["srcset"].split()[0]
            elif first_img.has_attr("src"):
                img_url_string = PREFIX_FOR_IMG + first_img.attrs["src"]

        summary = ""
        child_el = container.find(name="p")
        while child_el:
            if "h" in child_el.name:
                break
            if child_el.name == "p":
                summary += child_el.text + "\n"
            child_el = child_el.find_next_sibling()

        return UncyclopediaResult(heading, summary, img_url_string)



manager = UncyclopediaManager()

if __name__ == "__main__":
    random_url = "https://en.uncyclopedia.co/wiki/Special:RandomRootpage/Main"
    news_url = "https://en.uncyclopedia.co/wiki/UnNews:Ukraine_finally_does_something_in_war_with_Russia"
    result = manager.fetch(news_url)
    print(result)
