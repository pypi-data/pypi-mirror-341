from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="beaconpy",
    version="0.1.1",
    author="Fernando Rodriguez Romero",
    author_email="frr@keepcoding.io",
    description="A Pythonic implementation of the observer pattern",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/frr149/beaconpy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 