from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image-processing-dio-2025",
    version="0.0.1",
    author="castroxcode",
    description="Desafio Criando um Pacote de Processamento de Imagens com Python - DIO",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/castroxcode/image-processing-dio.git",
    packages=find_packages(),
    install_requires= requirements,
    python_requires='>=3.8',
)