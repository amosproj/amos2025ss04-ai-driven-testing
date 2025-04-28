from setuptools import setup, find_packages

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
