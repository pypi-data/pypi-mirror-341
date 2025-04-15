from setuptools import setup, find_packages

setup(
    name="nasaparser",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pdfplumber>=0.7.0",
        "pandas>=1.3.0"
    ],
    author="Siddhesh Phapale",
    author_email="rawsiddhesh11@gmail.com",
    description="NASA (Need Analysis)PDF Parser Library for extracting structured data",
    url="https://github.com/rawsid11/nasaparser",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
