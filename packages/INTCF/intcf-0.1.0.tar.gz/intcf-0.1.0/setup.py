from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='INTCF',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='cocoa',
    description='A Python module that will create the file provided if it doesn\'\t exist. ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)