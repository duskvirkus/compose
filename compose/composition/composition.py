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
        self.background: Color = None
        self._optimizers = None

        self.learning_rates: Dict = {
            'points': 1.0,
            'stroke_weight': 0.1,
            'stroke_color': 0.1,
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
            loss = analyzer(img, target)

            self._exporter.save(img, from_refine=True)

            print(f'loss: {loss.item()}')

            loss.backward()

            for optim in self._optimizers:
                optim.step()

            self.clamp_values()


    def _configure_optimizers(self) -> None:
        # traits = []
        # for el in self._elements:
        #     traits.extend(el.get_traits())

        # for t in traits:
        #     t.set_grad(True)

        # trait_types = {}
        # for t in traits:
        #     if t.type not in trait_types:
        #         trait_types[t.type] = []
        #     trait_types[t.type].append(t)
        
        # self._optimizers = {}
        # for type in trait_types:

        #     if type in self.learning_rates:
        #         lr = self.learning_rates[type]
        #     else:
        #         print('WARNING: {type} undefined in composition learning rates, using default.')
        #         lr = self.learning_rates['default']

        #     tensors = [t.data_ptr[0] for t in trait_types[type]]
        #     print(tensors)

        #     self._optimizers[type] = torch.optim.Adam(tensors, lr=lr)

        self._optimizers = []

        for type in self.learning_rates:
            lr = self.learning_rates[type]
            
            if type == 'points':
                points = []
                for el in self._elements:
                    points.extend(el.get_points())
        
                for a in points:
                    a.require_grad = True

                if len(points) > 0:
                    self._optimizers.append(torch.optim.Adam(points, lr=lr))

            elif type == 'stroke_weight':
                stroke_weights = []
                for el in self._elements:
                    stroke_weights.extend(el.get_stroke_weights())

                for a in stroke_weights:
                    a.require_grad = True

                if len(stroke_weights) > 0:
                    self._optimizers.append(torch.optim.Adam(stroke_weights, lr=lr))

            elif type == 'stroke_color':
                stroke_colors = []
                for el in self._elements:
                    stroke_colors.extend(el.get_stroke_colors())

                for a in stroke_colors:
                    a.require_grad = True
                
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


