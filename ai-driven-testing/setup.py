"""Installation and setup configuration for the AI-driven testing package.

This module contains the necessary setup information to install the package,
define its dependencies, and provide metadata about the project. It uses
setuptools to configure the package for distribution and installation.
"""

from setuptools import find_packages, setup

setup(
    name="ai-driven-testing",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An AI-driven testing application with a Hello World example.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # List your project dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
