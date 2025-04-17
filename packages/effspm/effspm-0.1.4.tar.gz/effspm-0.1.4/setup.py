import os
import setuptools
from setuptools import Extension
import pybind11

# Get the absolute path to the directory containing setup.py
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

ext_modules = [
    Extension(
        "effspm._core",
        sources=[
            os.path.join("effspm", "_core.cpp"),
            os.path.join("effspm", "load_inst.cpp"),
            os.path.join("effspm", "freq_miner.cpp"),
            os.path.join("effspm", "utility.cpp"),
        ],
        include_dirs=[
            pybind11.get_include(),
            os.path.join(BASE_DIR, "effspm"),  # Absolute path to the "effspm" folder
        ],
        language="c++",
        extra_compile_args=["-O3", "-std=c++17"],
    ),
]

setuptools.setup(
    name="effspm",
    version="0.1.4",  # keep in sync with pyproject.toml
    author="yeshu999",
    author_email="vootlayeswanth20@gmail.com",
    description="Prefix‑Projection sequential pattern mining",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yeshu999/effspm",
    packages=setuptools.find_packages(where="."),
    ext_modules=ext_modules,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=["pybind11>=2.6"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C++",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
