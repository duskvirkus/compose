# Compose

⚠️ This project is still in development. Please report bug but don't expect everything to work very smoothly.

A python module to streamline working with 2D and 3D vector graphics in machine learning projects.

Much of the philosophy of this module is based on [Processing](https://processing.org/) and [p5.js](https://p5js.org/). In other words it favors more accessible syntax over complete efficiency.

## Notebooks

Single Image Notebook: [./notebooks/compose_test_01_py.ipynb](./notebooks/compose_test_01_py.ipynb)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/duskvirkus/compose/blob/main/notebooks/compose_test_01_py.ipynb)

Video Notebook (very hacky): [./notebooks/compose_test_04_py.ipynb](./notebooks/compose_test_04_py.ipynb)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/duskvirkus/compose/blob/main/notebooks/compose_test_04_py.ipynb)

## Installing Locally

### Platform

Recommended python version is 3.7. Ubuntu based Linux is currently the only supported platform. If you run into issues on other platforms feel free to file an issue but it will be low priority.

### Anaconda Setup

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

## Documentation

Currently documentation could use some work and can only be built locally. See CONTRIBUTING.md for some instructions.

## Thanks

This project would not be possible without the work of the creators of diffvg Tzu-Mao Li, Michal Lukáč, Michaël Gharbi, and Jonathan Ragan-Kelley.

Thanks to Peter Schaldenbrand, Zhixuan Liu, Jean Oh (creators of StyleCLIPDraw) for example of getting diffvg working on colab.
