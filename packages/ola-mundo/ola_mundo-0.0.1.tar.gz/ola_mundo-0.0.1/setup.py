from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ola_mundo",
    version="0.0.1",
    author="jose_carlos_lima",
    description="Uma saudação para te livrar da maldição!",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/josecarloslima/DIO-Suzano-Python/tree/main/ola_mundo_pkg",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',    
    )