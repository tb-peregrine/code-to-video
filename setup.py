#!/usr/bin/env python3
"""
Setup script for code-to-video utility
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="code-to-video",
    version="1.0.0",
    author="Code to Video Generator",
    description="Convert markdown code blocks to typing animation videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/code-to-video",
    py_modules=["code_to_video"],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "code-to-video=code_to_video:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Documentation",
    ],
    python_requires=">=3.8",
) 