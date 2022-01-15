from enum import Enum
from typing import List

import torch

# class TraitType(Enum):
#     Points = 1,
#     StrokeWeight = 2,
#     StrokeColor = 3,
#     FillColor = 4,

class Trait:

    def __init__(
        self,
        data_ptr: List[torch.Tensor],
        type: str,
    ) -> None:
        if len(data_ptr) != 1:
            raise Exception('Invalid length for data_ptr. Intended to a singular tensor wrapped in a list to force pass by reference. Got {data_ptr}.')
        self.data_ptr: List[torch.Tensor] = data_ptr #[data_ptr[0]]
        self.type = type

    def set_grad(self, requires_grad):
        self.data_ptr[0].requires_grad = requires_grad

    def __str__(self) -> str:
        prefix = super().__str__()
        return f'{prefix}: [\n\ttype: {self.type}\n]'
