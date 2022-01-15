from abc import ABC, abstractmethod
from typing import List

from .trait import Trait

class Element(ABC):

    element_counter = 0

    @abstractmethod
    def get_traits(self):
        pass
    
    @abstractmethod
    def get_shape(self):
        pass

    @abstractmethod
    def get_shape_group(self):
        pass

    @abstractmethod
    def get_traits(self) -> List[Trait]:
        pass

    @abstractmethod
    def clamp_values(self) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        return super().__str__()

    @staticmethod
    def get_next_id() -> int:
        id = Element.element_counter
        Element.element_counter += 1
        return id