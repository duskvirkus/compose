from typing import Dict
from enum import Enum
from xml.dom.minidom import ProcessingInstruction

import pydiffvg
import torch

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
        learning_rates: Dict = {},
    ):
        self.width: int = width
        self.height: int = height
        self._renderer = renderer
        self._exporter = exporter
        self._elements = []

        # intentionally uninitialized
        self.background_color: Color = Color([255, 255, 255])
        self._optimizers = None

        self.learning_rates: Dict = {
            'points': 2.0,
            'stroke_weight': 0.05,
            'stroke_color': 0.2,
        }
        self.set_learning_rates(learning_rates)

    def add_element(self, el: Element) -> None:
        self._elements.append(el)
        self._optimizers = None

    def clamp_values(self) -> None:
        for el in self._elements:
            el.clamp_values()

    def set_learning_rates(
        self,
        learning_rates: Dict,
    ) -> None:
        for key in learning_rates:
            self.learning_rates[key] = learning_rates[key]
        self._optimizers = None

    def background(self, color: Color) -> None:
        self.background_color = color

    def refine(
        self,
        target: Image,
        analyzer: Analyzer,
        steps: int = 1,
    ) -> Image:
        if self._optimizers is None:
            self._configure_optimizers()
        for _ in range(steps):

            for optim in self._optimizers:
                optim.zero_grad()

            img = self._renderer.render(self)
            loss = analyzer(img, target, background=self.background_color)

            self._exporter.save(img.rgb(background_color=self.background_color), from_refine=True)

            print(f'loss: {loss.item()}')

            loss.backward()

            for optim in self._optimizers:
                optim.step()

            self.clamp_values()


    def _configure_optimizers(self) -> None:

        self._optimizers = []

        for type in self.learning_rates:
            lr = self.learning_rates[type]
            
            if type == 'points':
                points = []
                for el in self._elements:
                    points.extend(el.get_points())
        
                for a in points:
                    a.requires_grad = True

                if len(points) > 0:
                    self._optimizers.append(torch.optim.Adam(points, lr=lr))

            elif type == 'stroke_weight':
                stroke_weights = []
                for el in self._elements:
                    stroke_weights.extend(el.get_stroke_weights())

                for a in stroke_weights:
                    a.requires_grad = True

                if len(stroke_weights) > 0:
                    self._optimizers.append(torch.optim.Adam(stroke_weights, lr=lr))

            elif type == 'stroke_color':
                stroke_colors = []
                for el in self._elements:
                    stroke_colors.extend(el.get_stroke_colors())

                for a in stroke_colors:
                    a.requires_grad = True
                
                if len(stroke_colors) > 0:
                    self._optimizers.append(torch.optim.Adam(stroke_colors, lr=lr))

            else:
                raise Exception(f'ERROR: Unsupported learning rate type {type}.')

    def __len__(self) -> int:
        return len(self._elements)

    def __str__(self) -> str:
        prefix = super().__str__()
        return f'{prefix}: [\n\twidth: {self.width}\n\theight: {self.height}\n\telements: {self.__len__()}\n]'

    def get_scene_args(self):
        return pydiffvg.RenderFunction.serialize_scene(
            self.width,
            self.height,
            [element.get_shape() for element in self._elements],
            [element.get_shape_group() for element in self._elements],
        )
