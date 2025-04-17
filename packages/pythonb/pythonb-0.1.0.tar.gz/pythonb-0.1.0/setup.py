
from setuptools import setup, find_packages

setup(
    name="pythonb",
    version="0.1.0",
    author="Your Name",
    description="Integrity checker for name validation using tkinter",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pythonb",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
