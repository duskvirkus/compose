"""
Used for top level functions that don't fit well.

It also imports to make frequently used functions more accessible.
"""

# expose top level
from compose.chance.random import *
from compose.element.create import *
from compose.io import load
from compose.composition import Composition
from compose.render.type import RendererType
from compose.analyze.lpips import LPIPS

# for api functions
import typing
import os
import compose

def create_composition(
    width: int = 1920,
    height: int = 1080,
    renderer: typing.Union[compose.render.Renderer, RendererType] = RendererType.diffvg,
    exporter: compose.io.Exporter = None
) -> Composition:
    r"""Create a composition that contains differentiable vector elements.

    Will return a `Composition` object that manages a collection of elements and rendering.

    Parameters
    ----------
    width : int
        width of the ``Composition``.
    height : int
        height of the ``Composition``.
    renderer : {RendererType, compose.render.Renderer}, optional
        Rendering engine to use. Either provide one already constructed or specify one using a ``RendererType``.
    exporter : compose.io.Exporter, optional
        If you need to configure an optimizer then you can pass it in here otherwise a default one will be created.

    Returns
    -------
    Composition
        A ``Composition`` object used to keep track of and render elements.

    See Also
    --------
    compose.composition.Composition, compose.render.type.RenderType

    Notes
    -----

    References
    ----------

    Examples
    --------
    """
    if exporter is None:
        exporter = compose.io.Exporter(os.path.join(os.getcwd(), 'exports'))

    if type(renderer) != compose.render.Renderer:
        if renderer == RendererType.diffvg:
            renderer = compose.render.DiffVGRenderer()
        else:
            raise(f'ERROR: Unknown RenderType of {renderer} in create_composition()!')

    comp = Composition(width, height, renderer, exporter)

    return comp