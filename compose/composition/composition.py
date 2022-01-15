from typing import Union, List

import pydiffvg

from compose.image import Image
from compose.color import Color
from compose.element import Element
from compose.color import Color
from compose.analyze import Analyzer
from compose.render import Renderer
from compose.io import Exporter

class Composition:

    def __init__(
        self,
        width: int,
        height: int,
        renderer: Renderer,
        exporter: Exporter,
        background_color: Color = None,
    ):
        self.width: int = width
        self.height: int = height
        self._renderer = renderer
        self._exporter = exporter
        self._elements = []

        # intentionally uninitialized
        self.background: Color = None
        self._optimizers = None

    def add_element(self, el: Element) -> None:
        self._elements.append(el)
        self._optimizers = None

    def clamp_values(self) -> None:
        for el in self._elements:
            el.clamp_values()

    def refine(
        self,
        target: Image,
        analyzer: Analyzer,
        steps: int = 1,
    ) -> Image:
        for _ in range(steps):
            self.steps_since_export += 1

            for optim in self._optimizers:
                optim.zero_grad()

            img = self._renderer.render(self)
            loss = analyzer(img, target)

            self.exporter.save(img, from_refine=True)

            print(f'loss: loss.item()')

            loss.backward()

            for optim in self._optimizers:
                optim.step()

            self.clamp_values()


    def __len__(self) -> int:
        return len(self._elements)

    def __str__(self) -> str:
        prefix = super().__str__()
        return f'{prefix}: [\n\twidth: {self.width}\n\theight: {self.height}\n\telements: {self.__len__()}\n]'

    # def get_to_optimize(self) -> None:
    #     all_points = []
    #     all_stroke_widths = []
    #     all_colors = []
    #     for el in self.elements:
    #         points, stroke_widths, colors = el.get_to_optimize()
    #         all_points.extend(points)
    #         all_stroke_widths.extend(stroke_widths)
    #         all_colors.extend(colors)

    #     return all_points, all_stroke_widths, all_colors

    # def scene_args(self):
    #     self.cache_scene_args = pydiffvg.RenderFunction.serialize_scene(
    #         self.width,
    #         self.height,
    #         [element.get_shape() for element in self.elements],
    #         [element.get_shape_group() for element in self.elements],
    #     )
    #     return self.cache_scene_args


