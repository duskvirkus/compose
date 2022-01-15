from enum import Enum

class TraitType(Enum):
    Points = 1,
    StrokeWeight = 2,
    StrokeColor = 3,
    FillColor = 4,

class Trait:

    def __init__(
        self,
        data,
        type: TraitType,
    ) -> None:
        self.data = data
        self.type = type

    def set_grad(self, requires_grad):
        self.data.requires_grad = requires_grad
