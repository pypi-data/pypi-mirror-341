"""
Setup file for random_compliments package.
Created by a developer who may or may not have been replaced by a small shell script.
"""

from setuptools import setup, find_packages

# Package metadata - as reliable as weather forecasts
setup(
    name="random_compliments",
    version="0.1.0",  # Changed exactly once in the history of this package
    author="Boaz",
    author_email="probably.wont.read.this@example.com",
    description="A package that delivers compliments with the precision of a sleep-deprived pizza delivery person",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/random_compliments",  # As real as my vacation plans
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",  # Works on any machine capable of poor life choices
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",  # Because supporting Python 2 is like using a flip phone in 2023
    entry_points={
        "console_scripts": [
            "compliment=random_compliments.cli:main",  # Now you can get validation right from your terminal!
        ],
    },
) 