from typing import List, Union
import random

import numpy as np
import torch

from compose.element import Curve
from compose.element.create import create_continuous_curve

def rand(min = None, max = None):
    if min is None:
        min = 0
    if max is None:
        max = 1
    return random.random() * (max - min) + min;

def random_curve(
    segments: Union[int, List[int]],
    x_range: List[Union[int, float]],
    y_range: List[Union[int, float]],
    radius: float = 100.0,
    no_alpha: bool = False,
) -> Curve:

    if type(segments) == list and len(segments) == 2:
        segments = int(rand(segments[0], segments[1]))
    elif type(segments) == int:
        pass
    else:
        raise Exception('ERROR: Unexpected segments argument of {segments}. Expected single int or list of two int [min, max].')


    start = np.array([rand(x_range[0], x_range[1]), rand(y_range[0], y_range[1])], np.float32)

    points = np.zeros((segments, 2, 2), np.float32)

    previous = start
    for i in range(points.shape[0]):
        for j in range(points.shape[1]):
            points[i, j, 0] = previous[0] + radius * (rand() - 0.5)
            points[i, j, 1] = previous[1] + radius * (rand() - 0.5)
            previous = points[i, j, :]

    color = torch.tensor([
        rand(),
        rand(),
        rand(),
        1.0,
    ], dtype=torch.float32)

    width = torch.tensor(
        rand(min=1.0, max=8.0)
    )

    return create_continuous_curve(start, points, stroke_color=color, stroke_weight=width, no_alpha=no_alpha)