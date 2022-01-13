from typing import Union, List

import numpy as np

class Color:

    def __init__(
        self,
        data,
        max = 255.0,
    ) -> None:
        self.data = np.array(data)

        if self.data.shape[0] == 1:
            self.data = np.array([self.data[0] / max, self.data[0] / max, self.data[0] / max, 1.0])
        if self.data.shape[0] == 2:
            self.data = np.array([self.data[0] / max, self.data[0] / max, self.data[0] / max, self.data[1] / max])
        if self.data.shape[0] == 3:
            self.data = np.array([self.data[0] / max, self.data[1] / max, self.data[2] / max, 1.0])
        if self.data.shape[0] == 4:
            self.data /= max
