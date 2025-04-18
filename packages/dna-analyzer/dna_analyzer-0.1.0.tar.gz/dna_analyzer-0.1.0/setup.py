# setup.py
from setuptools import setup, find_packages

setup(
    name="dna_analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "biopython>=1.79",
        "numpy>=1.21.0",
        "pandas>=1.3.0"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for DNA sequence analysis in cancer research",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dna_analyzer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires=">=3.8",
)