from compose import *
import numpy as np

def test_create_line_xy():
    line = create_line(12, 34, 56, 78)

    assert line.data[0, 0] == 12
    assert line.data[0, 1] == 34
    assert line.data[1, 0] == 56
    assert line.data[1, 1] == 78

def test_create_line_list():
    line = create_line([12, 34], [56, 78])

    assert line.data[0, 0] == 12
    assert line.data[0, 1] == 34
    assert line.data[1, 0] == 56
    assert line.data[1, 1] == 78

def test_create_line_np():
    line = create_line(np.array([12, 34]), np.array([56, 78]))

    assert line.data[0, 0] == 12
    assert line.data[0, 1] == 34
    assert line.data[1, 0] == 56
    assert line.data[1, 1] == 78