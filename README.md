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
conda create -n compose python=3.7
conda activate compose
conda install -c conda-forge jupyterlab
conda install -c anaconda ipykernel
python -m ipykernel install --user --name=compose
```
### Dependancies

```bash
sudo ./scripts/install/platform/ubuntu.sh
sudo apt upgrade
git submodule update --init --recursive
python scripts/install/pytorch.py # to make sure you get the correct nvidia compile
pip install -r requirements.txt
cd diffvg
python setup.py install
cd ..
python setup.py install
```

## Thanks

This project would not be possible without the work of the creators of diffvg Tzu-Mao Li, Michal Lukáč, Michaël Gharbi, and Jonathan Ragan-Kelley.

Thanks to Peter Schaldenbrand, Zhixuan Liu, Jean Oh (creators of StyleCLIPDraw) for example of getting diffvg working on colab.
