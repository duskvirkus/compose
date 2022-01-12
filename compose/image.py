from typing import Union

import torch

class Image:

    def __init__(
        self,
        data: torch.Tensor
    ) -> None:
        self.data = data

        self.width = data.shape[1]
        self.height = data.shape[0]

def solid_image(width, height, color) -> Image:
    solid = torch.zeros((height, width, 3), dtype=torch.float32)

    solid[:, :, 0] = color[0]
    solid[:, :, 1] = color[1]
    solid[:, :, 2] = color[2]

    return Image(solid)