from os import device_encoding
from typing import Union

import torch
import pydiffvg
import cv2

from compose.color import Color

class Image:

    def __init__(
        self,
        data: torch.Tensor
    ) -> None:
        self.data = data

        self.width = data.shape[1]
        self.height = data.shape[0]

        self.lpips_cache = None
        self.lpips_cache_device = None

    def to_device(self, target: Union[torch.Tensor, str]) -> None:
        if type(target) == torch.Tensor:
            if self.data.device == target.device:
                return
            self.data = self.data.to(device=target.device)
            return
        if self.data.device == target:
            return
        self.data = self.data.to(device=target)

    def shape(self):
        return self.data.shape

    def rgb(self, background_color: Color = Color([255, 255, 255])):
        if self.data.shape[-1] == 3:
            return self.data
        assert(self.data.shape[-1] == 4) #TODO add support for more
        img = self.data
        background = solid_image(self.width, self.height, background_color, pydiffvg.get_device())
        transparency = torch.stack([img[:, :, -1] for _ in range(3)], axis=2)

        img = transparency * img[:, :, :3] + background * (1 - transparency)
        return img

    def for_lpips(self, device, use_cache = False):
        if self.lpips_cache is not None:
            if self.lpips_cache_device == device:
                return self.lpips_cache
            else:
                return self.lpips_cache.to(device)

        img = self.rgb()
        img = img.unsqueeze(0)
        img = img.permute(0, 3, 1, 2)
        img = img.to(device=device)

        if use_cache:
            self.lpips_cache = img
            self.lpips_cache_device = device

        return img

def solid_image(width, height, color: Color, device = 'cpu') -> Image:
    solid = torch.zeros((height, width, 3), dtype=torch.float32, device=device)

    solid[:, :, 0] = color.data[0]
    solid[:, :, 1] = color.data[1]
    solid[:, :, 2] = color.data[2]

    return solid