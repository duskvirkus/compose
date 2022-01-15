from typing import List, Union
from compose.element import curve

import torch
import numpy as np

from compose.element.curve import Curve
from compose.color import Color
from compose import random

### Line ###

def create_line_xy(
    x1: Union[int, float],
    y1: Union[int, float],
    x2: Union[int, float],
    y2: Union[int, float],
    stroke_color: Union[Color, torch.Tensor] = torch.tensor([0.5, 0.5, 0.5, 1.0]),
    stroke_weight: Union[int, float, torch.Tensor] = torch.tensor(1.0),
) -> Curve:
    return create_line(np.array([x1, y1]), np.array([x2, y2]), stroke_color, stroke_weight)

def create_line(
    start: Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    end: Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    stroke_color: Union[Color, torch.Tensor] = torch.tensor([0.5, 0.5, 0.5, 1.0], dtype=torch.float32),
    stroke_weight: Union[int, float, torch.Tensor] = torch.tensor(1.0, dtype=torch.float32),
) -> Curve:
    if type(end) == list:
        end = [end]
    elif type(end) == np.ndarray:
        end = np.expand_dims(end, axis=0)
    else:
        end = end.unsqueeze(0)
    return create_continuous_curve(start, end, stroke_color, stroke_weight)

### Curve ###

def create_curve_xy(
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
    return create_curve(np.array([x1, y1]), np.array([x2, y2]), np.array([x3, y3]), np.array([x4, y4]), stroke_color, stroke_weight)

def create_curve(
    start: Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    control_1: Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    control_2: Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    end: Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    stroke_color: Union[Color, torch.Tensor] = torch.tensor([0.5, 0.5, 0.5, 1.0], dtype=torch.float32),
    stroke_weight: Union[int, float, torch.Tensor] = torch.tensor(1.0, dtype=torch.float32),
) -> Curve:

    if type(start) != torch.Tensor:
        start = torch.tensor(start, dtype=torch.float32)
    if type(control_1) != torch.Tensor:
        control_1 = torch.tensor(control_1, dtype=torch.float32)
    if type(control_2) != torch.Tensor:
        control_2 = torch.tensor(control_2, dtype=torch.float32)
    if type(end) != torch.Tensor:
        end = torch.tensor(end, dtype=torch.float32)
    
    curve_data = torch.cat([
        control_1,
        control_2,
        end,
    ]).to(dtype=torch.float32).unsqueeze(0)

    return create_continuous_curve(start, curve_data, stroke_color, stroke_weight)

def create_continuous_curve(  
    start:  Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    curve_data: Union[List[List[List[Union[int, float]]]], np.ndarray, torch.Tensor],
    stroke_color: Union[Color, torch.Tensor] = torch.tensor([0.5, 0.5, 0.5, 1.0], dtype=torch.float32),
    stroke_weight: Union[int, float, torch.Tensor] = torch.tensor(1.0, dtype=torch.float32),
) -> Curve:

    if type(curve_data) == list:
        curve_data = np.array(curve_data, np.float32)
    
    num_control_points = torch.zeros(curve_data.shape[0], dtype = torch.int32) + curve_data.shape[1]

    curve_data = curve_data.reshape((-1, 2))

    if type(curve_data) == np.ndarray:
        curve_data = torch.from_numpy(curve_data)

    if type(start) == list:
        start = torch.tensor(start, dtype=torch.float32)
    elif type(start) == np.ndarray:
        start = torch.from_numpy(start)

    start = start.unsqueeze(0)

    curve_data = torch.cat((start, curve_data), 0)

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
