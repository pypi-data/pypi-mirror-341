from setuptools import setup, find_packages

# Read the content of README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yadu",
    version="0.1.0",
    packages=find_packages(),
    description="A simple package that prints 'IOS DEVELOPER' when imported",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yaduraj",
    author_email="yadurajsingham@gmail.com",
    url="https://github.com/YadurajManu",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 