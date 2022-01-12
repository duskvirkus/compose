import torch
import pydiffvg

class Path(pydiffvg.Path):

    def __init__(
        self,
        num_control_points,
        points,
        is_closed: bool,
        stroke_width: torch.Tensor = torch.tensor(1.0),
        id = '',
        use_distance_approx: bool = False
    ):
      super().__init__(num_control_points, points, is_closed, stroke_width, id, use_distance_approx)