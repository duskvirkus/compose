from abc import ABC, abstractmethod

from ..image import Image

class Renderer(ABC):
    
    @abstractmethod
    def render(self) -> Image:
        pass
