import subprocess

CUDA_version = [s for s in subprocess.check_output(["nvcc", "--version"]).decode("UTF-8").split(", ") if s.startswith("release")][0].split(" ")[-1]
print("CUDA version:", CUDA_version)

if CUDA_version == "10.0":
    torch_version_suffix = "+cu100"
elif CUDA_version == "10.1":
    torch_version_suffix = "+cu101"
elif CUDA_version == "10.2":
    torch_version_suffix = "+cu102"
else:
    torch_version_suffix = "+cu110"

subprocess.call(['pip', 'install', f'torch==1.7.1{torch_version_suffix}', f'torchvision==0.8.2{torch_version_suffix}', '-f', 'https://download.pytorch.org/whl/torch_stable.html'])
