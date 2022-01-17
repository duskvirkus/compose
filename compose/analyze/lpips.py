import lpips
import torch
import numpy as np

from compose.image import Image
from compose.color import Color
from .analyzer import Analyzer

class LPIPS(Analyzer):
    
    def __init__(
        self,
        net = 'vgg'
    ) -> None:
        self.net = None
        self.set_net(net)

        self.loss_function = None
        self.on_gpu = False

    def configure(self) -> None:
        self.loss_function = lpips.LPIPS(net=self.net, version='0.1')
        if torch.cuda.is_available():
            self.loss_function.cuda()
            self.on_gpu = True

    def get_device(self) -> str:
        if self.on_gpu:
            return torch.cuda.current_device()
        return 'cpu'
        
    def analyze(self, img, target, background: Color):
        if self.loss_function is None:
            self.configure()
        a = img.for_lpips(self.get_device(), background_color=background)
        b =  target.for_lpips(self.get_device(), True, background_color=background)
        return self.loss_function(a, b)

    def set_net(self, net: str) -> None:
        if net == 'alex' or net == 'vgg':
            if net != self.net:
                self.net = net
                self.loss_function = None
        else:
            raise Exception(f"ERROR! lpips got an unknown net type of \'{net}\', options are 'alex' or 'vgg'.")