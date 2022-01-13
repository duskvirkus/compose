import lpips
import torch
import numpy as np

from .image import Image

class LPIPS:
    
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

    def __call__(
        self,
        img: Image,
        target: Image,
    ):
        return self.compare(img, target)

    def get_device(self) -> str:
        if self.on_gpu:
            return torch.cuda.current_device()
        return 'cpu'
        
    def compare(self, img, target):
        if self.loss_function is None:
            self.configure()
        # img.to_device(self.get_device())
        # target.to_device(self.get_device())

        # a = img.rgb()
        # a = a.unsqueeze(0)
        # a = a.permute(0, 3, 1, 2)
        # a = a.to(device=self.get_device())
        a = img.for_lpips(self.get_device())

        # b = target.rgb()
        # b = b.unsqueeze(0)
        # b = b.permute(0, 3, 1, 2)
        # b = b.to(device=self.get_device())
        b =  img.for_lpips(self.get_device(), True)

        # b = target.rgb()[:, :, :, np.newaxis].transpose((3, 2, 0, 1))
        return self.loss_function(a, b)

    def set_net(self, net: str) -> None:
        if net == 'alex' or net == 'vgg':
            if net != self.net:
                self.net = net
                self.loss_function = None
        else:
            raise Exception(f"ERROR! lpips got an unknown net type of \'{net}\', options are 'alex' or 'vgg'.")
