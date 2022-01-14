from abc import ABC, abstractmethod

from ..image import Image

class Analyzer:

    def __call__(
        self,
        img: Image,
        target: Image
    ):
        return self.analyze(img, target)

    @abstractmethod
    def analyze(
        self,
        img: Image,
        target: Image
    ):
        pass

