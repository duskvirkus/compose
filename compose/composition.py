from elements.path import Path

class Composition:

    def __init__(
        self,
        width: int = 100,
        height: int = 100,
    ):
        self.width = width
        self.height = height

        self.elements = []

    def add_path(self, p: Path) -> None:
        self.elements.append(p)

    def __len__(self) -> int:
        return len(self.elements)

    def __str__(self) -> str:
        prefix = super().__str__()
        return f'{prefix}: [\n\twidth: {self.width}\n\theight: {self.height}\n\telements: {self.__len__()}\n]'
