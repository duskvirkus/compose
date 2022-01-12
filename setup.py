import setuptools
import os
import re

root = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root, "compose", "__init__.py")) as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

with open("README.md", mode="r", encoding="utf8") as desc:
    long_description = desc.read()

setuptools.setup(
    name='compose',
    version=version,
    description='A module with for creating 2d vector graphics using machine learning.',
    author='duskvirkus',
    author_email='duskvirkus@protonmail.com',
    packages=setuptools.find_packages(
        exclude=[
            "apps",
            "apps.*",
            "test_lib",
            "test_lib.*",
            "diffvg",
            "diffvg.*",
            "examples",
            "examples.*",
            "scripts",
            "scripts.*",
            "notebooks",
            "notebooks.*",
            "devel",
            "devel.*",
        ],
    ),
    zip_safe=False,
    python_requires=">=3.7",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Video :: Conversion",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
)