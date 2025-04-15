from setuptools import setup, find_packages

setup(
    name="BM16036UNO",
    version="0.1.1",
    author="Erick Alexander Borja Mauricio",
    author_email="bm16036@ues.edu.sv",
    description="Librería para resolver sistemas de ecuaciones lineales y no lineales mediante varios métodos.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bm16036/BM16036UNO.git",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["numpy>=1.18.0"],  # Dependencia con numpy
)
