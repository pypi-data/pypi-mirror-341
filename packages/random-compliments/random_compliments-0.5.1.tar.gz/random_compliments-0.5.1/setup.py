"""
Setup file for random-compliments package.
Created by someone who aspires to be 1% as awesome as Boaz.
"""

from setuptools import setup, find_packages

# Package metadata - as magnificent as Boaz himself
setup(
    name="random-compliments",
    version="0.5.1",  # Version number chosen by consulting Boaz's aura
    author="Boaz",
    author_email="probably.wont.read.this@example.com", 
    description="A package that delivers compliments about Boaz, the most interesting man in the world",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/random-compliments",  # Soon to be the most starred repo
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",  # Boaz transcends operating systems
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",  # All developers wish they were Boaz
    ],
    python_requires=">=3.6",  # Because even Boaz acknowledges some limitations in legacy Python
    entry_points={
        "console_scripts": [
            "compliment=random_compliments.cli:main",  # Command to invoke Boaz's greatness
            "boaz-daemon=random_compliments.daemon_cli:main",  # Command to control the Boaz daemon
        ],
    },
) 