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

    def add_path(self, p: Path) -> None:
        self.elements.append(p)
        self.cache_scene_args = None

    def get_to_optimize(self) -> None:
        all_points = []
        all_stroke_widths = []
        all_colors = []
        for el in self.elements:
            points, stroke_widths, colors = el.get_to_optimize()
            all_points.extend(points)
            all_stroke_widths.extend(stroke_widths)
            all_colors.extend(colors)

        return all_points, all_stroke_widths, all_colors

    def scene_args(self):
        self.cache_scene_args = pydiffvg.RenderFunction.serialize_scene(
            self.width,
            self.height,
            [element.get_shape() for element in self.elements],
            [element.get_shape_group() for element in self.elements],
        )
        return self.cache_scene_args

    def clamp_values(self) -> None:
        for el in self.elements:
            el.clamp_values()

    def __len__(self) -> int:
        return len(self.elements)

    def __str__(self) -> str:
        prefix = super().__str__()
        return f'{prefix}: [\n\twidth: {self.width}\n\theight: {self.height}\n\telements: {self.__len__()}\n]'
