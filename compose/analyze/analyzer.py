from abc import ABC, abstractmethod

from compose.image import Image
from compose.color import Color

class Analyzer:

    def __call__(
        self,
        img: Image,
        target: Image,
        background: Color,
    ):
        return self.analyze(img, target, background)

    @abstractmethod
    def analyze(
        self,
        img: Image,
        target: Image,
        background: Color,
    ):
        pass

