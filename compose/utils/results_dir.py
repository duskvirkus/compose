import os
import re


def create_results_dir(results_root: str, results_name: str):
    os.makedirs(results_root, exist_ok=True)

    max_num = -1
    for root, subdirs, files in os.walk(results_root):
        for subdir in subdirs:
            numbers = re.findall('[0-9]+', subdir)
            if numbers:
                if (int(numbers[0]) > max_num):
                    max_num = int(numbers[0])
    
    max_num += 1

    results_dir = os.path.join(results_root, str(max_num).zfill(6) + '-' + results_name)
    os.makedirs(results_dir)
    return results_dir