import os
import re
from setuptools import setup, find_packages

def get_version():
    # Get version from git tag if available
    version = os.environ.get('GITHUB_REF', '')
    if version.startswith('refs/tags/v'):
        return version.split('/')[-1][1:]  # Remove 'v' prefix
    return "0.0.5" 

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Read README.md for long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pudim_hunter_driver_scraper",
    version=get_version(),
    description="Playwright-based scraper implementation for The Pudim Hunter platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Luis Machado Reis",
    author_email="luis.reis@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Source": "https://github.com/luismr/pudim-hunter-driver-scraper",
        "Bug Tracker": "https://github.com/luismr/pudim-hunter-driver-scraper/issues",
    }
) 