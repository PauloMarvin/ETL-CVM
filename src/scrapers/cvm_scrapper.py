import re
from io import BytesIO
from typing import List, Union, Dict
from urllib.request import urlopen
from zipfile import ZipFile

import pandas as pd
from bs4 import BeautifulSoup, NavigableString

from src.scrapers.interface.scrapper_interface import ScrapperInterface
from src.soups.soup_generator import Soup


class CvmScrapper(ScrapperInterface):
    def __init__(self, configured_soup: Soup) -> None:
        self.soup = configured_soup

    def get_first_element(self, html_tag: str) -> BeautifulSoup | NavigableString | None:
        return self.soup.soup_obj.find(html_tag)

    def get_all_elements(self, html_tags: Union[str, list], tag_class: Dict[str, str],
                         another_soup: BeautifulSoup) -> list:
        if another_soup is None:
            return self.soup.soup_obj.find_all(html_tags, {'class': tag_class})
        else:  # caso o objeto BeautifulSoup tenha sido obtido por outro objeto BeautifulSoup.
            return another_soup.find_all(html_tags, {'class': tag_class})

    def get_all_links(self) -> List[str]:
        links = []
        for link in self.soup.soup_obj.find_all('a'):
            temp_url = link.get('href')
            match = re.match("^(http://|https://)", temp_url)
            if match:
                url = temp_url
            else:
                url = f"{self.soup.url}{temp_url}"
            links.append(url)

        if len(links) == 0:
            print(f"No links found in {self.soup.url}")

        if len(links) == 1:
            links = links[0]

        return links

    def filter_links(self, patterns: Union[list, str]) -> List[str]:
        if isinstance(patterns, str):
            patterns = [patterns]
        filtered_links = []
        for link in self.get_all_links():
            for pattern in patterns:
                if pattern in link:
                    filtered_links.append(link)

        if len(filtered_links) == 0:
            print(f"No links found in {self.soup.url} with the pattern(s) {patterns}")

        if len(filtered_links) == 1:
            filtered_links = filtered_links[0]
        return filtered_links

    @staticmethod
    def load_zip_file_from_url(url: str) -> ZipFile:
        response = urlopen(url)
        print(f"Downloading zip file from {url}")
        zip_file_obj = ZipFile(BytesIO(response.read()))
        return zip_file_obj

    @staticmethod
    def generate_data_frame_from_zip_file(zip_file: ZipFile) -> pd.DataFrame:
        dataframe = pd.DataFrame()
        file_names = zip_file.namelist()
        print(f"Processing zip with this files:\n{zip_file.namelist()}")
        for file_name in file_names:
            if file_name.endswith(".csv"):
                temp_file = zip_file.read(f"{file_name}")
                temp_dataframe = pd.read_csv(BytesIO(temp_file), sep=";", encoding="utf-8")
                dataframe = pd.concat([dataframe, temp_dataframe], ignore_index=True)

        return dataframe
