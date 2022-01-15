import pydiffvg
import numpy as np

from compose.render import Renderer
from compose.image import Image

class DiffVGRenderer(Renderer):

    def __init__(self) -> None:
        super().__init__()

        self.render_backend = pydiffvg.RenderFunction.apply
        self.seed = 0

    def render(
        self,
        comp,
    ) -> Image:

        return Image(self.render_backend(
            comp.width,
            comp.height,
            2,
            2,
            self.seed,
            None,
            *comp.scene_args()
        ))
        