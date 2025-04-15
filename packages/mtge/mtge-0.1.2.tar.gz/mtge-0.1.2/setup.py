## Directory Structure:
# project_name/
# ├── mtge/
# │   ├── __init__.py
# │   ├── xux64.py
# │   └── libxux64.so
# ├── setup.py
# ├── MANIFEST.in
# ├── README.md
# └── pyproject.toml (optional)

# ------------------------
# File: mtge/__init__.py
# ------------------------
# Leave empty or include logic to expose library

# ------------------------
# File: mtge/xux64.py
# ------------------------
import os
import ctypes

# Dynamic path to shared object
_lib_path = os.path.join(os.path.dirname(__file__), "mtge/libxux64.so")
lib = ctypes.CDLL(_lib_path)

# Example function from shared object
# lib.your_function_name.argtypes = [ctypes.c_int]
# lib.your_function_name.restype = ctypes.c_int

# ------------------------
# File: setup.py
# ------------------------
from setuptools import setup, find_packages

setup(
    name="mtge",
    version="0.1.2",
    author="Beyondbond",
    author_email="info@beyondbond.com",
    description="Python mortgage calculation library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "mtge": ["libxux64.so"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

# ------------------------
# File: MANIFEST.in
# ------------------------
# include mtge/libxux64.so

# ------------------------
# File: README.md
# ------------------------
## mtge

# This is a Python wrapper for the `libxux64.so` shared library using ctypes.

# ------------------------
# Optional: pyproject.toml (if using PEP 517/518 build tools)
# ------------------------
# [build-system]
# requires = ["setuptools", "wheel"]
# build-backend = "setuptools.build_meta"

# ------------------------
# Build and Upload Commands (run in project root)
# ------------------------
# pip install build twine
# python3 -m build
# python3 -m twine upload dist/*
