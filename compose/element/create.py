from typing import List, Union

import torch
import numpy as np
from multipledispatch import dispatch

from compose.element.curve import Curve
from compose.color import Color
from compose import random

def default_stroke_color() -> torch.Tensor:
    return torch.tensor([
        0.5,
        0.5,
        0.5,
        1.0,
    ])

### Line ###

@dispatch(
    Union[int, float],
    Union[int, float],
    Union[int, float],
    Union[int, float],
    Union[Color, torch.Tensor],
    Union[int, float, torch.Tensor],
)
def create_line(
    x1: Union[int, float],
    y1: Union[int, float],
    x2: Union[int, float],
    y2: Union[int, float],
    stroke_color: Union[Color, torch.Tensor] = torch.tensor([0.5, 0.5, 0.5, 1.0]),
    stroke_weight: Union[int, float, torch.Tensor] = torch.tensor(1.0),
) -> Curve:
    return create_line(np.array([x1, y1]), np.array([x2, y2]), stroke_color, stroke_weight)

@dispatch(
    Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    Union[Color, torch.Tensor],
    Union[int, float, torch.Tensor],
)
def create_line(
    start: Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    end: Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    stroke_color: Union[Color, torch.Tensor] = torch.tensor([0.5, 0.5, 0.5, 1.0]),
    stroke_weight: Union[int, float, torch.Tensor] = torch.tensor(1.0),
) -> Curve:
    if type(end) == List:
        end = [end]
    return create_continuous_curve(start, end, stroke_color, stroke_weight)

### Curve ###

@dispatch(
    Union[int, float],
    Union[int, float],
    Union[int, float],
    Union[int, float],
    Union[int, float],
    Union[int, float],
    Union[int, float],
    Union[int, float],
    Union[Color, torch.Tensor],
    Union[int, float, torch.Tensor],
)
def create_curve(
    x1: Union[int, float],
    y1: Union[int, float],
    x2: Union[int, float],
    y2: Union[int, float],
    x3: Union[int, float],
    y3: Union[int, float],
    x4: Union[int, float],
    y4: Union[int, float],
    stroke_color: Union[Color, torch.Tensor] = torch.tensor([0.5, 0.5, 0.5, 1.0]),
    stroke_weight: Union[int, float, torch.Tensor] = torch.tensor(1.0),
) -> Curve:
    create_line(np.array([x1, y1]), np.array([x2, y2]), np.array([x3, y3]), np.array([x4, y4]), stroke_color, stroke_weight)

@dispatch(
    Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    Union[Color, torch.Tensor],
    Union[int, float, torch.Tensor],
)
def create_curve(
    start: Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    control_1: Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    control_2: Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    end: Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    stroke_color: Union[Color, torch.Tensor] = torch.tensor([0.5, 0.5, 0.5, 1.0]),
    stroke_weight: Union[int, float, torch.Tensor] = torch.tensor(1.0),
) -> Curve:
    return create_continuous_curve(start, np.array([control_1, control_2, end]), stroke_color, stroke_weight)

def create_continuous_curve(  
    start:  Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    curve_data: Union[List[List[List[Union[int, float]]]], np.ndarray, torch.Tensor],
    stroke_color: Union[Color, torch.Tensor] = torch.tensor([0.5, 0.5, 0.5, 1.0]),
    stroke_weight: Union[int, float, torch.Tensor] = torch.tensor(1.0),
) -> Curve:

    if type(curve_data) == List:
        curve_data = np.array(curve_data)
    
    num_control_points = torch.zeros(curve_data.shape[0], dtype = torch.int32) + curve_data.shape[1]

    curve_data = curve_data.reshape((-1, 2))

    if type(curve_data) == np.ndarray:
        curve_data = torch.from_numpy(curve_data)

    if type(start) == List:
        start = torch.tensor(start)
    elif type(start) == np.ndarray:
        start = torch.from_numpy(start)

    curve_data = torch.cat((start, curve_data), 0)

    # if type(points) == np.ndarray:
    #     points = torch.from_numpy(points)
    # elif type(points) != torch.Tensor:
    #     points = torch.tensor(points)

    # if type(stroke_color) == Color:
    #     stroke_color = stroke_color.as_tensor()

    # if type(stroke_weight) != torch.tensor:
    #     stroke_weight = torch.tensor(stroke_weight)

    # num_control_points = torch.zeros(points.shape[0], dtype = torch.int32) + 2

    return Curve(
        num_control_points = num_control_points,
        points = curve_data,
        stroke_color = stroke_color,
        stroke_width = stroke_weight,
    )

def random_curve(
    segments: Union[int, List[int]],
    x_range: List[Union[int, float]],
    y_range: List[Union[int, float]],
    radius: float = 0.05,
    clamp: bool = False,
) -> Curve:

    if type(segments) == List and len(segments) == 2:
        segments = int(random(segments[0], segments[1]))
    elif type(segments) == int:
        pass
    else:
        raise Exception('ERROR: Unexpected segments argument of {segments}. Expected single int or list of two int [min, max].')

    points = np.zeros()

    p0 = (random(x_range), random(y_range))
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
