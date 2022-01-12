
# def check_image_extension(p: str) -> bool:
#     ext = p.split('.')[-1]
#     return ext == 'png' or ext == 'jpg' or ext == 'jpeg'

# def get_image_paths(input_paths: List[str]) -> List[str]:
#     image_paths = []
#     for input in input_paths:
#         if os.path.isfile(input):
#             if check_image_extension(input):
#                 image_paths.append(input)
#             else:
#                 print(f'WARNING. Skipping {input}. Unsupported file extension.')

#         elif os.path.isdir(input):
#             for root, _, files in sorted(os.walk(input)):
#                 for f in files:
#                     if check_image_extension(f):
#                         image_paths.append(os.path.join(root, f))
#                     else:
#                         print(f'WARNING: Unsupported file extension. Skipping {os.path.join(root, f)}.')

#         else:
#             print(f'WARNING: Not found. Skipping {i}')

#     return image_paths

class Loader:

    def __init__(self):
        print('loader')