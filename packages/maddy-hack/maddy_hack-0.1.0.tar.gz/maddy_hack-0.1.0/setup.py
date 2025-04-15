# setup.py
from setuptools import setup, find_packages

setup(
    name="maddy_hack",  # Package name on PyPI
    version="0.1.0",
    description="A package to compute nearest meeting cells, largest cycle sums, and max weight nodes from an edge array.",
    author="Mandar Kelkar",
    author_email="mandarkelkar0@gmail.com",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'maddy-hack=maddy_hack:main',  # This lets users run `custom-model` from the command line.
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
