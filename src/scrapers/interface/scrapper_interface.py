from abc import ABC, abstractmethod
from typing import List


class ScrapperInterface(ABC):

    @abstractmethod
    def get_all_links(self) -> List[str]:
        raise NotImplementedError("Should implement method : get_links")

    @abstractmethod
    def filter_links(self, pattern: str) -> List[str]:
        raise NotImplementedError("Should implement method : filter_links")
