"""
Script de instalación para Image Merger Tool
"""

from setuptools import setup, find_packages
import os

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="image-merger-tool",
    version="1.0.0",
    description="Una aplicación para combinar múltiples imágenes en una sola",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Frandy",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'image-merger=src.main:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)