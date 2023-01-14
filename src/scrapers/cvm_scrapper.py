from bs4 import BeautifulSoup

from src.scrapers.interface.scrapper_interface import ScrapperInterface
from src.soups.soup_generator import Soup
from typing import List, Union, Dict
import re

class CvmScrapper(ScrapperInterface):
    def __init__(self, configured_soup: Soup) -> None:
        self.soup = configured_soup

    def get_first_element(self, html_tag: str) -> List[str]:
        return self.soup.soup_obj.find(html_tag)

    def get_all_elements(self, html_tags: Union[str,list],tag_class: Dict[str,str] , another_soup : BeautifulSoup) -> None:
        if another_soup == None:
            return self.soup.find_all(html_tags, {'class': tag_class})
        else:  # caso o objeto BeautifulSoup tenha sido obtido por outro objeto BeautifulSoup.
            return another_soup.find_all(html_tags, {'class': tag_class})

    def get_links(self) -> List[str]:
        """Retrieve all the links of the page"""
        links = []
        for link in self.soup.soup_obj.find_all('a'):
            temp_url = link.get('href')
            match = re.match(("^(http:\/\/|https:\/\/)"), temp_url)
            if match:
                url = temp_url
            else:
                url = self.soup.url + temp_url
            links.append(url)
        return links

    def filter_links(self, patterns: Union[list, str]) -> List[str]:
        """Filter the links based on a pattern and return the matching links"""

        if isinstance(patterns, str):
            patterns = [patterns]
        filtered_links = []
        for link in self.get_links():
            for pattern in patterns:
                if pattern in link:
                    filtered_links.append(link)
        return filtered_links

