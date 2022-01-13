from .composition import Composition
from .image import Image

class Refinery:

    def __init__(
        self,
        step_size: int = 1,
        export = False,
    ) -> None:

        self.step_size = step_size
        self.export = export

    def __call__(
        self,
        comp: Composition,
        target: Image,
    ):
        self.step(comp, target) 

    def step(
        self,
        comp: Composition,
        target: Image,
    ) -> None:
        for i in range(self.step_size):
            pass
