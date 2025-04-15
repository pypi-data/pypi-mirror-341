from setuptools import setup, find_packages

setup(
    name="IA22001UNO",
    version="0.1.0",
    author="Michelle Iglesias",
    author_email="ia22001@ues.edu.sv",
    description="Creación de una librería para resolver sistemas de ecuaciones lineales y ecuaciones no lineales",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ia22001MichelleIglesias/IA22001UNO",
    packages=find_packages(),
    install_requires=["numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)