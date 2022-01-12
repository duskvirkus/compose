import os
from typing import Union

from typing import Union, List

import torch
import cv2

def check_image_extension(p: str) -> bool:
    ext = p.split('.')[-1]
    return ext == 'png' or ext == 'jpg' or ext == 'jpeg'    

def pre_process_paths(paths: Union[str, List[str]]) -> List[str]:
    if type(paths) == str:
        return [os.path.abspath(paths)]
    return [os.path.abspath(path) for path in paths]

def get_image_paths(input_paths: List[str]) -> List[str]:
    image_paths = []
    for input in input_paths:
        if os.path.isfile(input):
            if check_image_extension(input):
                image_paths.append(input)
            else:
                print(f'WARNING. Skipping {input}. Unsupported file extension.')

        elif os.path.isdir(input):
            for root, _, files in sorted(os.walk(input)):
                for f in files:
                    if check_image_extension(f):
                        image_paths.append(os.path.join(root, f))
                    else:
                        print(f'WARNING: Unsupported file extension. Skipping {os.path.join(root, f)}.')

        else:
            print(f'WARNING: Not found. Skipping {input}')

    return image_paths

def load(
    to_load: Union[str, List[str]]
) -> Union[torch.Tensor, List[torch.Tensor]]:

    image_paths = get_image_paths(pre_process_paths(to_load))

    images = [torch.from_numpy(cv2.imread(path)).to(torch.float32) / 255.0 for path in image_paths]

    if len(images) < 1:
        raise Exception(f'ERROR: Unable to load any images! {to_load}')
    elif len(images) == 1:
        return images[0]
    else:
        return images
