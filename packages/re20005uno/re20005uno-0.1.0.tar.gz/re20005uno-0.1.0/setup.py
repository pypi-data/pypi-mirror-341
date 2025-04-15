 
from setuptools import setup, find_packages

setup(
    name="re20005uno",
    version="0.1.0",
    author="Gerson",
    description="Librería de métodos numéricos para sistemas de ecuaciones",
    long_description="Esta librería implementa métodos numéricos como Bisección, Eliminación de Gauss, Gauss-Seidel, Cramer, entre otros.",
    long_description_content_type="text/markdown",
    url="https://github.com/re20005/re20005uno",  
    packages=find_packages(),
    install_requires=[
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)