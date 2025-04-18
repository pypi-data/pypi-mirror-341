import sys
from setuptools import find_packages, setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="logs-py-solutions",
    version="0.1.1",
    packages=find_packages(where="logs-py-solutions"),
    package_dir={"": "logs_py_solutions"},
    author="Bruker BioSpin GmbH & Co KG",
    author_email="support@sciy.com",
    description="Prebuild solution library for the logs-py package",
    long_description=(this_directory / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://docs.logs-python.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
    ],
    python_requires='>=3.8',
    install_requires=[
        "logs-py>=3.0.6",
    ],
)
