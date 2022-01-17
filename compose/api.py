# expose top level
from compose.chance.random import *
from compose.element.create import *
from compose.io import load
from compose.composition import Composition
from compose.render.type import RendererType
from compose.analyze.lpips import LPIPS
from compose.analyze.multi import MultiAnalyzer
from compose.analyze.blob import BlobAnalyzer

# for api functions
import typing
import os
import compose

def create_composition(
    width: int = 1920,
    height: int = 1080,
    renderer: typing.Union[compose.render.Renderer, RendererType] = RendererType.diffvg,
    exporter: compose.io.Exporter = None,
) -> Composition:

    if exporter is None:
        exporter = compose.io.Exporter(os.path.join(os.getcwd(), 'exports'))

    if type(renderer) != compose.render.Renderer:
        if renderer == RendererType.diffvg:
            renderer = compose.render.DiffVGRenderer()
        else:
            raise(f'ERROR: Unknown RenderType of {renderer} in create_composition()!')

    comp = Composition(width, height, renderer, exporter)

    return comp