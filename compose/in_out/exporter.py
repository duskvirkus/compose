import os
import re

import cv2
import numpy as np

from compose.image import Image

class Exporter:

    def __init__(
        self,
        export_root: str,
        postfix: str = None,
    ):
        self.export_root = export_root
        self.postfix = postfix

        self.run_directory = None

        self.export_count = 0

    def create_run_directory(self) -> None:
        os.makedirs(self.export_root, exist_ok=True)

        max_num = -1
        for _, subdirs, _ in os.walk(self.export_root):
            for subdir in subdirs:
                numbers = re.findall('[0-9]+', subdir)
                if numbers:
                    if (int(numbers[0]) > max_num):
                        max_num = int(numbers[0])

        max_num += 1

        run_name = str(max_num).zfill(9)
        if self.postfix:
            run_name += '-' + self.postfix
        self.run_directory = os.path.join(self.export_root, run_name)

        os.makedirs(self.run_directory)

    def save(
        self,
        to_export: Image,
        name: str = 'export',
    ) -> None:
        if self.run_directory is None:
            self.create_run_directory()

        image = to_export.data.detach().numpy()
        image *= 255
        image = image.astype(np.uint8)
        cv2.imwrite(os.path.join(self.run_directory, str(self.export_count).zfill(6) + '-' + name + '.png'), image, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        self.export_count += 1
