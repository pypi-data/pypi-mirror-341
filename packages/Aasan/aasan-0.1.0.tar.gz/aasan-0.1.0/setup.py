from setuptools import setup, find_packages

setup(
    name="Aasan",
    version="0.1.0",
    author="Aneesh Shukla",
    author_email="aneeshshukla.tech@gmail.com",
    description="This python package helps make python more easier than it already is.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    #url="https://github.com/aneeshshukla/aasan",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
