
from setuptools import setup, find_packages

setup(
    name="mscnltk",  # Package name
    version="0.1",
    packages=find_packages(),
    description="A package to display and retrieve NLTK question codes",
    long_description="This package includes a list of questions and their corresponding codes in NLTK for NLP tasks.",
    long_description_content_type="text/markdown",
    author="FitByIT",
    author_email="fitbyit@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
             "mscnltk=mscnltk.cli:main",  # This line sets up the command
        ]
    },
)
