from urllib.request import urlopen

from bs4 import BeautifulSoup


class Soup:
    def __init__(self, url: str):
        self.url: str = url
        self.soup_obj: BeautifulSoup = self.__generate_soup_obj()

    def __generate_soup_obj(self):
        response = urlopen(self.url)  # requisição.
        html = response.read().decode("utf-8")
        return BeautifulSoup(html, "html.parser")

    def get_soup_html(self, prettify: bool = False):
        if prettify:
            return self.soup_obj.prettify()
        else:
            return str(self.soup_obj)
