from typing import List

import torch
import pydiffvg

from compose.element.element import Element
from compose.element.trait import Trait, TraitType

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

    def get_traits(self) -> List[Trait]:
        traits = []

        traits.append(Trait(self.shape.points, TraitType.Points))
        traits.append(Trait(self.shape.stroke_width, TraitType.StrokeWeight))
        traits.append(Trait(self.shape_group.stroke_color, TraitType.StrokeColor))

        return traits

    def get_shape(self):
        return self.shape

    def get_shape_group(self):
        return self.shape_group

    def clamp_values(self) -> None:
        self.shape_group.stroke_color.data.clamp_(0.0, 1.0)
