import random

import torch

from .composition import Composition
from .elements.curve import Curve

def random_curve(
    comp: Composition
) -> Curve:

    num_segments = random.randint(3, 5)
    num_control_points = torch.zeros(num_segments, dtype = torch.int32) + 2
    points = []
    p0 = (random.random(), random.random())
    points.append(p0)
    for j in range(num_segments):
        radius = 0.05
        p1 = (p0[0] + radius * (random.random() - 0.5), p0[1] + radius * (random.random() - 0.5))
        p2 = (p1[0] + radius * (random.random() - 0.5), p1[1] + radius * (random.random() - 0.5))
        p3 = (p2[0] + radius * (random.random() - 0.5), p2[1] + radius * (random.random() - 0.5))
        points.append(p1)
        points.append(p2)
        if j < num_segments - 1:
            points.append(p3)
            p0 = p3
    points = torch.tensor(points)
    points[:, 0] *= comp.width
    points[:, 1] *= comp.height

    stroke_color = torch.tensor([
        random.random(),
        random.random(),
        random.random(),
        random.random(),
    ])

    return Curve(
        num_control_points = num_control_points,
        points = points,
        stroke_color = stroke_color,
        stroke_width = torch.tensor(1.0),
    )

def random_curve_composition(
    num_curves: int,
    width: int = 100,
    height: int = 100,
) -> Composition:

    comp = Composition(width, height)

    for i in range(num_curves):
        comp.add_path(random_curve(comp))

    return comp

