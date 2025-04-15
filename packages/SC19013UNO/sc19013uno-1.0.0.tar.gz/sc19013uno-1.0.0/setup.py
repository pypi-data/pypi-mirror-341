from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="SC19013UNO",
    version="1.0.0",
    author="Luis Serpas",
    author_email="sc19013@ues.edu.sv",
    description="Librería de métodos numéricos para resolver sistemas de ecuaciones lineales y no lineales",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ACamposWeb/sc19013uno",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],  # No requiere dependencias externas
)