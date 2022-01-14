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
    import pydiffvg
    import torch
    from .in_out.load import load
    from .in_out.exporter import Exporter
    from .composition import Composition
    from .random import random_curve, random_curve_composition
    from .render.default import DefaultRenderer
    from .image import Image
    from .anazlyze import LPIPS
    from .refine import Refinery
    from .render.renderer import Renderer

    global exporter
    global renderer
    global lpips
    global refinery

    exporter = Exporter(os.path.join(os.getcwd(), 'exports'))
    renderer = DefaultRenderer()
    lpips = LPIPS()
    refinery = Refinery()

    pydiffvg.set_use_gpu(torch.cuda.is_available())

    def render(comp: Composition) -> Image:
        return renderer.render(comp)

    def save(img: Image) -> None:
        exporter.save(img)

    def refine(
        comp: Composition,
        img: Image,
        renderer: Renderer = renderer,
        analyzer = lpips,
        exporter: Exporter = exporter,
    ) -> None:
        refinery(comp, img, renderer, analyzer, exporter)

    def export_init(comp) -> None:
        img = render(comp)
        exporter.save(img, 'init')

    def export_steps(every: int = 1) -> None:
        refinery.set_export(export_every=every)