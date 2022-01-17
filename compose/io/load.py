import os
from typing import Union

from typing import Union, List

import torch
import cv2
import numpy as np

from ..image import Image

def check_image_extension(p: str) -> bool:
    r"""TODO short description

    TODO long description

    Parameters
    ----------
    p : str
        String to check.

    Returns
    -------
    bool
        True the path is directed at a image with a supported file extension or False it is not.

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    References
    ----------
    TODO

    Examples
    --------
    TODO
    """
    ext = p.split('.')[-1]
    return ext == 'png' or ext == 'jpg' or ext == 'jpeg'    

def pre_process_paths(paths: Union[str, List[str]]) -> List[str]:
    r"""TODO short description

    TODO long description

    Parameters
    ----------
    paths : Union[str, List[str]]
        Single string or list of strings to be pre processed.

    Returns
    -------
    List[str]
        List of strings with absolute paths.

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    References
    ----------
    TODO

    Examples
    --------
    TODO
    """
    if type(paths) == str:
        return [os.path.abspath(paths)]
    return [os.path.abspath(path) for path in paths]

def get_image_paths(input_paths: List[str]) -> List[str]:
    """TODO short description

    TODO long description

    Parameters
    ----------
    input_paths : List[str]
        List of paths to be checked.

    Returns
    -------
    List[str]
        Paths filtered to only include supported images.

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    References
    ----------
    TODO

    Examples
    --------
    TODO
    """
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
) -> Union[Image, List[Image]]:
    """TODO short description

    TODO long description

    Parameters
    ----------
    to_load : Union[str, List[str]]
        Path(s) to image that should be loaded.

    Returns
    -------
    Union[Image, List[Image]]
        Image(s) that were loaded.

    See Also
    --------
    TODO

    Notes
    -----
    TODO

    References
    ----------
    TODO

    Examples
    --------
    TODO
    """
    image_paths = get_image_paths(pre_process_paths(to_load))

    images = [Image(torch.from_numpy(cv2.imread(path)).to(torch.float32) / 255.0) for path in image_paths]

    if len(images) < 1:
        raise Exception(f'ERROR: Unable to load any images! {to_load}')
    elif len(images) == 1:
        return images[0]
    else:
        return images
