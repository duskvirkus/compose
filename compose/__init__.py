__version__ = "0.0.1"

try:
    compose_mode
except NameError:
    mode = 'normal'
else:
    if compose_mode == 'barebones' or compose_mode == 'normal':
        mode = compose_mode
    else:
        raise Exception(f'ERROR: Unknown compose_mode {compose_mode}. ')

if mode == 'normal':
    import os
    from .in_out.load import load
    from .in_out.exporter import Exporter
    from .composition import Composition
    from .random import random_curve, random_curve_composition
    from .renderer.default import DefaultRenderer
    from .image import Image

    global exporter
    global renderer

    exporter = Exporter(os.path.join(os.getcwd(), 'exports'))
    renderer = DefaultRenderer()

    def render(comp: Composition) -> Image:
        return renderer.render(comp)

    def save(img: Image) -> None:
        exporter.save(img)