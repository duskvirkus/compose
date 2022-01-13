import pydiffvg
import numpy as np

from .renderer import Renderer
from ..composition import Composition
from ..image import Image, solid_image


class DefaultRenderer(Renderer):

    def __init__(self) -> None:
        super().__init__()

        self.render_backend = pydiffvg.RenderFunction.apply

        self.seed = 0
        self.background_color = None

    def render(
        self,
        comp: Composition
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

    def background(
        self,
        color,
        range_max: float = 255.0
    ) -> None:
        if len(color) == 3:
            self.background_color = np.array(color, np.float32)
            self.background_color /= range_max

        