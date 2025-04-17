from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys
import os



# Read README safely
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="fytly",
    version="1.0.6",
    author="chowdeswari seelam",
    author_email="chowdeswari_seelam@aegletek.com",
    description='A grading component for keyword-based scoring for resume',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3',
    packages=find_packages(),
    #package_dir={'': 'py'},
    license='MIT',
    install_requires=[
        'PyPDF2',
        'python-docx',
        'scikit-learn',
        'pyspellchecker',
        'stanza',
        'nltk',
        'rapidfuzz',
        ],

)
