#src/shared_logic/setup.py
from setuptools import setup, find_packages

setup(
    name='hdsemg-shared',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
    ]
)