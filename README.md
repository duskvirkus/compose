# Compose

⚠️ This project is a work in progress and is likely to be buggy and maybe abandon if it doesn't make sense.

A module with scripts and jupyter/colab notebooks for creating 2d vector graphics using machine learning.

## Notebooks

Image to SVG Notebook

`coming soon`

Image to Plotter SVG

`coming soon`

Create Animation

`coming soon`

## Installing Locally

For a more streamlined process use jupyter lab and vanilla jupyter notebooks.

### Python Config

Recommended python version is 3.7. Ubuntu based Linux is currently the only supported platform. If you run into issues on other platforms feel free to file an issue but it will be low priority.

*If you use Anaconda*
```bash
conda create -n pg python=3.7
conda activate pg
```
*If python is installed natively you may need to run*
```bash
alias python=python3
alias pip=pip3
```

### Dependancies

```bash
./scripts/install/platform/ubuntu.sh
git submodule update --init --recursive
python pytorch.py # to make sure you get the correct nvidia compile
pip install -r requirements.txt
cd diffvg
python setup.py install
cd ..
python setup.py install
```

## Thanks

This project would not be possible without the work of the creators of diffvg Tzu-Mao Li, Michal Lukáč, Michaël Gharbi, and Jonathan Ragan-Kelley.

Thanks to Peter Schaldenbrand, Zhixuan Liu, Jean Oh (creators of StyleCLIPDraw) for example of getting diffvg working on colab.

openFrameworks for borrowed setup script examples
