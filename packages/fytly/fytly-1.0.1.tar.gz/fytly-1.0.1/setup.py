from setuptools import setup, find_packages

setup(
    name="fytly",
    version="1.0.1",
    author="chowdeswari seelam",
    author_email="chowdeswari_seelam@aegletek.com",
    description='A grading component for keyword-based scoring for resume',
    classifiers=['Programming Language :: Python :: 3',
                 'Operating System :: OS Independent',],
    python_requires='>=3',
    packages=find_packages(),
    package_dir={
        '': '.',  # Important for your flat structure
        'grader.py': 'py',
        'grader.api': 'api'},
    license='MIT',
    install_requires=['']

)