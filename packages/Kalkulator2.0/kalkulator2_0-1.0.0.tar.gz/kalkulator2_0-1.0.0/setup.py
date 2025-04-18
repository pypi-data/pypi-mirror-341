from setuptools import setup, find_packages

setup(
    name = "Kalkulator2.0",
    version = "1.0.0",
    author = "Victor",
    author_email = "",
    description = "A simple calculator package for practice",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    url = "",
    packages = find_packages(),
    install_requires = [],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.6',
)