from abc import ABC, abstractmethod
from typing import List


class ScrapperInterface(ABC):

    @abstractmethod
    def get_first_element(self, html_tag: str):
        raise NotImplementedError("Should implement method : get_first_element")
    @abstractmethod
    def get_all_elements(self, html_tag: str) -> None:
        raise NotImplementedError("Should implement method : get_all_elements")

    @abstractmethod
    def get_links(self) -> List[str]:
        raise NotImplementedError("Should implement method : get_links")

    @abstractmethod
    def filter_links(self, pattern: str) -> List[str]:
        raise NotImplementedError("Should implement method : filter_links")



