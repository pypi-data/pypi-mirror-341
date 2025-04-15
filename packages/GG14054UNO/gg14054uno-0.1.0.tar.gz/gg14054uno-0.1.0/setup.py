from setuptools import setup, find_packages

setup(
    name="GG14054UNO",
    version="0.1.0",
    author="Walter Galicia",
    author_email="gg14054@ues.edu.sv",
    description="Librería para resolver sistemas de ecuaciones lineales y no lineales. Corto CAD135",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LexterDev/GG14054UNO",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "scipy",
    ],
)