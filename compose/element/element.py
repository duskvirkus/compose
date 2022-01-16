from abc import ABC, abstractmethod
from typing import List

import torch

class Element(ABC):

    element_counter = 0
    
    @abstractmethod
    def get_shape(self):
        pass

    @abstractmethod
    def get_shape_group(self):
        pass

    @abstractmethod
    def clamp_values(self) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        return super().__str__()

    @abstractmethod
    def get_points(self) -> List[torch.Tensor]:
        pass

    @abstractmethod
    def get_stroke_weights(self) -> List[torch.Tensor]:
        pass

    @abstractmethod    
    def get_stroke_colors(self) -> List[torch.Tensor]:
        pass

    @staticmethod
    def get_next_id() -> int:
        id = Element.element_counter
        Element.element_counter += 1
        return id