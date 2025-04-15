from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the version from __init__.py
with open(os.path.join("telecomfaker", "__init__.py"), "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break
    else:
        version = "0.1.0"  # Default if not found

setup(
    name="telecomfaker",
    version=version,
    author="Stefan Stuehrmann",
    author_email="stefan.stuehrmann@outlook.com",
    description="A Python package for generating realistic telecom operator test data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StefanStuehrmann/telecomfaker",
    project_urls={
        "Bug Tracker": "https://github.com/StefanStuehrmann/telecomfaker/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Communications",
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "telecomfaker": ["data/*.json"],
    },
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=1.10.8,<=2.11.3",
    ],
    entry_points={
        "console_scripts": [
            "telecomfaker=telecomfaker.cli:main",
        ],
    },
) 