from compose import *
import numpy as np
import torch

from pytest import approx

def test_create_line_xy_int():
    line = create_line_xy(12, 34, 56, 78)

    assert type(line) == Curve

    points = line.get_points()
    assert points[0, 0] == 12
    assert points[0, 1] == 34
    assert points[1, 0] == 56
    assert points[1, 1] == 78

def test_create_line_xy_float():
    line = create_line_xy(1.2, 3.4, 5.6, 7.8)

    assert type(line) == Curve

    points = line.get_points()
    assert points[0, 0].item() == approx(1.2)
    assert points[0, 1].item() == approx(3.4)
    assert points[1, 0].item() == approx(5.6)
    assert points[1, 1].item() == approx(7.8)

def test_create_line_list_int():
    line = create_line([12, 34], [56, 78])

    assert type(line) == Curve

    points = line.get_points()
    assert points[0, 0] == 12
    assert points[0, 1] == 34
    assert points[1, 0] == 56
    assert points[1, 1] == 78

def test_create_line_list_float():
    line = create_line([1.2, 3.4], [5.6, 7.8])

    assert type(line) == Curve

    points = line.get_points()
    assert points[0, 0].item() == approx(1.2)
    assert points[0, 1].item() == approx(3.4)
    assert points[1, 0].item() == approx(5.6)
    assert points[1, 1].item() == approx(7.8)

def test_create_line_np():
    line = create_line(np.array([12, 34]), np.array([56, 78]))

    assert type(line) == Curve

    points = line.get_points()
    assert points[0, 0] == 12
    assert points[0, 1] == 34
    assert points[1, 0] == 56
    assert points[1, 1] == 78

def test_create_line_torch():
    line = create_line(torch.tensor([12, 34]), torch.tensor([56, 78]))

    assert type(line) == Curve

    points = line.get_points()
    assert points[0, 0] == 12
    assert points[0, 1] == 34
    assert points[1, 0] == 56
    assert points[1, 1] == 78

def test_create_curve_xy_int():
    curve = create_curve_xy(1, 2, 3, 4, 5, 6)

    assert type(curve) == Curve

    points = curve.get_points()
    assert points[0, 0] == 1
    assert points[0, 1] == 2
    assert points[1, 0] == 3
    assert points[1, 1] == 4
    assert points[2, 0] == 5
    assert points[2, 1] == 6

def test_create_curve_xy_float():
    curve = create_curve_xy(0.1, 0.2, 0.3, 0.4, 0.5, 0.6)

    assert type(curve) == Curve

    points = curve.get_points()
    assert points[0, 0].item() == approx(.1)
    assert points[0, 1].item() == approx(.2)
    assert points[1, 0].item() == approx(.3)
    assert points[1, 1].item() == approx(.4)
    assert points[2, 0].item() == approx(.5)
    assert points[2, 1].item() == approx(.6)

def test_create_curve_list_int():
    curve = create_curve([1, 2], [3, 4], [5, 6])

    assert type(curve) == Curve

    points = curve.get_points()
    assert points[0, 0] == 1
    assert points[0, 1] == 2
    assert points[1, 0] == 3
    assert points[1, 1] == 4
    assert points[2, 0] == 5
    assert points[2, 1] == 6

def test_create_curve_list_float():
    curve = create_curve([0.1, 0.2], [0.3, 0.4], [0.5, 0.6])

    assert type(curve) == Curve

    points = curve.get_points()
    assert points[0, 0].item() == approx(.1)
    assert points[0, 1].item() == approx(.2)
    assert points[1, 0].item() == approx(.3)
    assert points[1, 1].item() == approx(.4)
    assert points[2, 0].item() == approx(.5)
    assert points[2, 1].item() == approx(.6)

def test_create_curve_np():
    curve = create_curve(
        np.array([1, 2]),
        np.array([3, 4]),
        np.array([5, 6]),
    )

    assert type(curve) == Curve

    points = curve.get_points()
    assert points[0, 0] == 1
    assert points[0, 1] == 2
    assert points[1, 0] == 3
    assert points[1, 1] == 4
    assert points[2, 0] == 5
    assert points[2, 1] == 6

def test_create_curve_torch():
    curve = create_curve(
        torch.tensor([1, 2]), 
        torch.tensor([3, 4]), 
        torch.tensor([5, 6]), 
    )

    assert type(curve) == Curve

    points = curve.get_points()
    assert points[0, 0] == 1
    assert points[0, 1] == 2
    assert points[1, 0] == 3
    assert points[1, 1] == 4
    assert points[2, 0] == 5
    assert points[2, 1] == 6

def test_create_continuous_curve_list_int():
    curve = create_continuous_curve(
        [11, 12], 
        [[
                [13, 14], 
                [15, 16], 
            ],[
                [17, 18],
                [19, 20], 
            ],
        ],
    )

    assert type(curve) == Curve

    points = curve.get_points()
    assert points[0, 0] == 11
    assert points[0, 1] == 12
    assert points[1, 0] == 13
    assert points[1, 1] == 14
    assert points[2, 0] == 15
    assert points[2, 1] == 16
    assert points[3, 0] == 17
    assert points[3, 1] == 18
    assert points[4, 0] == 19
    assert points[4, 1] == 20

def test_create_continuous_curve_list_float():
    curve = create_continuous_curve(
        [1.1, 1.2], 
        [[
                [1.3, 1.4], 
                [1.5, 1.6], 
            ],[
                [1.7, 1.8],
                [1.9, 2.0], 
            ],
        ],
    )

    assert type(curve) == Curve

    points = curve.get_points()
    assert points[0, 0].item() == approx(1.1)
    assert points[0, 1].item() == approx(1.2)
    assert points[1, 0].item() == approx(1.3)
    assert points[1, 1].item() == approx(1.4)
    assert points[2, 0].item() == approx(1.5)
    assert points[2, 1].item() == approx(1.6)
    assert points[3, 0].item() == approx(1.7)
    assert points[3, 1].item() == approx(1.8)
    assert points[4, 0].item() == approx(1.9)
    assert points[4, 1].item() == approx(2.0)

def test_create_continuous_curve_np():
    curve = create_continuous_curve(
        np.array([11, 12]), 
        np.array([[
                [13, 14], 
                [15, 16], 
            ],[
                [17, 18],
                [19, 20], 
            ],
        ]),
    )

    assert type(curve) == Curve

    points = curve.get_points()
    assert points[0, 0] == 11
    assert points[0, 1] == 12
    assert points[1, 0] == 13
    assert points[1, 1] == 14
    assert points[2, 0] == 15
    assert points[2, 1] == 16
    assert points[3, 0] == 17
    assert points[3, 1] == 18
    assert points[4, 0] == 19
    assert points[4, 1] == 20

def test_create_continuous_curve_torch():
    curve = create_continuous_curve(
        torch.tensor([11, 12]), 
        torch.tensor([[
                [13, 14], 
                [15, 16], 
                [17, 18],
            ],[
                [19, 20], 
                [21, 22], 
                [23, 24],
            ],
        ]),
    )

    assert type(curve) == Curve

    points = curve.get_points()
    assert points[0, 0] == 11
    assert points[0, 1] == 12
    assert points[1, 0] == 13
    assert points[1, 1] == 14
    assert points[2, 0] == 15
    assert points[2, 1] == 16
    assert points[3, 0] == 17
    assert points[3, 1] == 18
    assert points[4, 0] == 19
    assert points[4, 1] == 20
