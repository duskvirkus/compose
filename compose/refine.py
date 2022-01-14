import torch

from .composition import Composition
from .image import Image
from .render.renderer import Renderer
from .in_out.exporter import Exporter
from .analyze.analyzer import Analyzer

class Refinery:

    def __init__(
        self,
        step_size: int = 1,
        export = False,
    ) -> None:

        self.step_size = step_size
        self.export = export
        self.steps_since_export = 0
        self.export_every = 1

        self.points_optimizer = None
        self.width_optimizer = None
        self.color_optimizer = None

    def __call__(
        self,
        comp: Composition,
        target: Image,
        renderer: Renderer,
        analyzer: Analyzer,
        exporter: Exporter,
    ):
        self.step(comp, target, renderer, analyzer, exporter)

    def setup_optimizers(
        self,
        comp: Composition,
    ) -> None:
        points, stroke_widths, colors = comp.get_to_optimize()

        self.points_optimizer = torch.optim.Adam(points, lr=1.0)
        self.width_optimizer = torch.optim.Adam(stroke_widths, lr=0.1)
        self.color_optimizer = torch.optim.Adam(colors, lr=0.01)

    def set_export(
        self,
        export: bool = True,
        export_every: int = 1,
    ) -> None:
        self.export = export
        self.export_every = export_every

    def step(
        self,
        comp: Composition,
        target: Image,
        renderer: Renderer,
        analyzer: Analyzer,
        exporter: Exporter,
    ) -> None:
        for i in range(self.step_size):
            self.steps_since_export += 1

            self.points_optimizer.zero_grad()
            self.width_optimizer.zero_grad()
            self.color_optimizer.zero_grad()

            img = renderer.render(comp)

            loss = analyzer(img, target)

            if self.export and self.steps_since_export >= self.export_every:
                exporter.save(img)
                self.steps_since_export = 0
                print('export')

            print(loss.item())

            loss.backward()

            comp.clamp_values()
