from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="CA21062UNO",
    version="1.1.0",
    author="Luis Cea",
    author_email="luiscea04@gmail.com",
    description="Librería creada para la resolución de métodos numéricos para resolver sistemas lineales y no lineales",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.19.0",
        "scipy>=1.7.1",
    ],

)