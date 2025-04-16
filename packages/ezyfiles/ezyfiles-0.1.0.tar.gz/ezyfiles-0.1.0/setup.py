from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ezyfiles",
    version="0.1.0",
    author="Kaustubh Raykar",
    author_email="raykarkaustubh@gmail.com",
    description="Truly Simple File Operations for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Raykarr/ezyfiles",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas>=1.3.0",
        "openpyxl>=3.0.0",
        "pyyaml>=6.0",
    ],
)   