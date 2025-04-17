from setuptools import setup
import os

# Read README for long description
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name="fytly",
    version="1.0.9",  # Update version as needed
    author="chowdeswari seelam",
    author_email="chowdeswari_seelam@aegletek.com",
    description="A grading component for keyword-based scoring for resumes",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    packages=["scorer","configs"],  # Explicitly list your package
    package_dir={"": "."},  # Important for proper package discovery
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "PyPDF2",
        "python-docx",
        "pyspellchecker",
        "stanza",
        "nltk",
        "rapidfuzz",
    ],
    # Optional if you have non-Python files to include
    package_data={
        "scorer": ["*.txt", "*.md","*.properties"],
    },
)