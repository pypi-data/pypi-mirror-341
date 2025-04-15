from setuptools import setup, find_packages
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="Nemotron",
    version="0.1.1",
    packages=find_packages(),
    install_requires=["requests"],
    author="Ramona-Flower",
    description="A wrapper for NEMOTRON chat and images API, Accountless!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ramona-Flower/Nemotron4free",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
