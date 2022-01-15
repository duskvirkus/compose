from typing import List, Union
from compose.element import curve

import torch
import numpy as np

from compose.element.curve import Curve
from compose.color import Color

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
    stroke_color: Union[Color, torch.Tensor] = torch.tensor([0.5, 0.5, 0.5, 1.0]),
    stroke_weight: Union[int, float, torch.Tensor] = torch.tensor(1.0),
) -> Curve:
    return create_curve(np.array([x1, y1]), np.array([x2, y2]), np.array([x3, y3]), stroke_color, stroke_weight)

def create_curve(
    start: Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    control: Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    end: Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    stroke_color: Union[Color, torch.Tensor] = torch.tensor([0.5, 0.5, 0.5, 1.0], dtype=torch.float32),
    stroke_weight: Union[int, float, torch.Tensor] = torch.tensor(1.0, dtype=torch.float32),
) -> Curve:

    if type(start) != torch.Tensor:
        start = torch.tensor(start, dtype=torch.float32)
    if type(control) != torch.Tensor:
        control = torch.tensor(control, dtype=torch.float32)
    if type(end) != torch.Tensor:
        end = torch.tensor(end, dtype=torch.float32)
    
    curve_data = torch.cat([
        control,
        end,
    ]).to(dtype=torch.float32).unsqueeze(0)

    return create_continuous_curve(start, curve_data, stroke_color, stroke_weight)

def create_continuous_curve(  
    start:  Union[List[Union[int, float]], np.ndarray, torch.Tensor],
    curve_data: Union[List[List[List[Union[int, float]]]], np.ndarray, torch.Tensor],
    stroke_color: Union[Color, torch.Tensor] = torch.tensor([0.5, 0.5, 0.5, 1.0], dtype=torch.float32),
    stroke_weight: Union[int, float, torch.Tensor] = torch.tensor(1.0, dtype=torch.float32),
) -> Curve:

    if type(start) != torch.Tensor:
        start = torch.tensor(start, dtype=torch.float32)

    if type(curve_data) != torch.Tensor:
        curve_data = torch.tensor(curve_data, dtype=torch.float32)

    assert curve_data.ndim == 3
    
    num_control_points = torch.zeros(curve_data.shape[0], dtype = torch.int32) + curve_data.shape[1] - 1

    curve_data = curve_data.reshape((-1, 2))

    start = start.unsqueeze(0)

    curve_data = torch.cat((start, curve_data), 0)

    return Curve(
        num_control_points = num_control_points,
        points = curve_data,
        stroke_color = stroke_color,
        stroke_width = stroke_weight,
    )
