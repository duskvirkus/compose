from typing import List

import torch
import pydiffvg

from compose.element.element import Element
from compose.element.trait import Trait

class Curve(Element):

    def __init__(
        self,
        num_control_points,
        points,
        stroke_color: torch.Tensor,
        stroke_width: torch.Tensor = torch.tensor(1.0),
        id = None,
        use_distance_approx: bool = False
    ):
        if id is None:
            id = Element.get_next_id()
        
        if stroke_color.shape[0] is not 4:
            raise(Exception(f'ERROR: expected stroke_color to have shape[0] == 4 but got {stroke_color.shape[0]}'))

        self.shape = pydiffvg.Path(
            num_control_points,
            points,
            False,
            stroke_width,
            id,
            use_distance_approx
        )

        self.shape_group = pydiffvg.ShapeGroup(
            shape_ids = torch.tensor([id]),
            fill_color = None,
            stroke_color = stroke_color,
        )

    def get_points(self) -> List[torch.Tensor]:
        return [self.shape.points]

    def get_stroke_weights(self) -> List[torch.Tensor]:
        return [self.shape.stroke_width]
    
    def get_stroke_colors(self) -> List[torch.Tensor]:
        return [self.shape_group.stroke_color]

    def get_traits(self) -> List[Trait]:
        traits = []

        traits.append(Trait([self.shape.points], 'points'))
        traits.append(Trait([self.shape.stroke_width], 'stroke_weight'))
        traits.append(Trait([self.shape_group.stroke_color], 'stroke_color'))

        return traits

    def get_shape(self):
        return self.shape

    def get_points(self) -> torch.Tensor:
        return self.shape.points

    def get_shape_group(self):
        return self.shape_group

    def clamp_values(self) -> None:
        self.shape_group.stroke_color.data.clamp_(0.0, 1.0)

    def __str__(self) -> str:
        prefix = super().__str__()
        return f'{prefix}: [\n\tpoints: {self.get_points()}\n]'
