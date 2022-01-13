import pydiffvg

from .elements.path import Path
from .image import Image

class Composition:

    def __init__(
        self,
        width: int = 100,
        height: int = 100,
    ):
        self.width = width
        self.height = height

        self.elements = []

        self.cache_scene_args = None

        # optimizers

    def add_path(self, p: Path) -> None:
        self.elements.append(p)
        self.cache_scene_args = None

    def scene_args(self):
        # print(self.elements[0].shape())
        # print([element.shape() for element in self.elements])
        if self.cache_scene_args is None:
            self.cache_scene_args = pydiffvg.RenderFunction.serialize_scene(
                self.width,
                self.height,
                [element.get_shape() for element in self.elements],
                [element.get_shape_group() for element in self.elements],
            )
        return self.cache_scene_args

    def __len__(self) -> int:
        return len(self.elements)

    def __str__(self) -> str:
        prefix = super().__str__()
        return f'{prefix}: [\n\twidth: {self.width}\n\theight: {self.height}\n\telements: {self.__len__()}\n]'
