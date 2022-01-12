import os
import re

class Exporter:

    def __init__(
        self,
        export_root: str,
        postfix: str = None,
    ):
        self.export_root = export_root
        self.postfix = postfix

        self.run_directory = None
        self.create_run_directory()

    def create_run_directory(self) -> None:
        os.makedirs(self.export_root, exist_ok=True)

        max_num = -1
        for root, subdirs, files in os.walk(self.export_root):
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
