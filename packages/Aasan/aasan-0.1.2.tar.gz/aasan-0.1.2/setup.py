from setuptools import setup, find_packages
long_desc = open("README.md").read()
setup(
    name="Aasan",
    version="0.1.2",
    author="Aneesh Shukla",
    description="This python package helps make python more easier than it already is.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/aneeshshukla/aasan",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
