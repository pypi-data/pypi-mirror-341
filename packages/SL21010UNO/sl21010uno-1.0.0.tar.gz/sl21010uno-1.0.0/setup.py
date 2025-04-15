from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="SL21010UNO",
    version="1.0.0",
    author="EnzoSanchez",
    author_email="sl21010@ues.edu.sv",
    description="Librería de métodos numéricos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SL21010-prn335-cicloII-2022/SL21010UNO.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.19.0",
],

)