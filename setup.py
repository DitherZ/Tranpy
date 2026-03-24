#!/usr/bin/env python3

"""
TranPy - Advanced Document Translation Tool
Setup configuration for package installation
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file (if exists)
readme_file = Path(__file__).parent / "README.md"
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")
else:
    long_description = "Advanced document translation tool with intelligent processing"

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
else:
    requirements = [
        "deep-translator>=1.11.4",
        "pdfminer.six>=20231228",
        "python-docx>=1.1.0",
        "tqdm>=4.66.0",
        "requests>=2.31.0",
        "aiohttp>=3.9.0",
        "urllib3>=2.1.0",
    ]

setup(
    name="tranpy",
    version="2.0.0",
    author="DitherZ",
    author_email="blackflame@example.com",
    description="Advanced multi-format document translation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DitherZ/tranpy",
    packages=find_packages(),
    py_modules=["tranpy"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "tranpy=tranpy.tranpy:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
