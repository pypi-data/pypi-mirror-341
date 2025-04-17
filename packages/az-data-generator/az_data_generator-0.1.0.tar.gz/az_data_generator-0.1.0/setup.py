from setuptools import setup, find_packages
import os

# Чтение содержимого README.md для длинного описания
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="az-data-generator",
    version="0.1.0",
    author="LocalDoc",
    author_email="v.resad.89@gmail.com",
    description=(
        "A comprehensive Python library for generating realistic test data for Azerbaijan, "
        "including personal identification, banking, geographical, and contact information. "
        "Designed for developers, testers, and data scientists who need high-quality, realistic test data "
        "that follows Azerbaijani formats and standards."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LocalDoc-Azerbaijan/az-data-generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Укажите зависимости, если они есть (например, "requests>=2.20")
    ],
    include_package_data=True,
    package_data={
        "data_generator": ["data/*.json"],
    },
)
