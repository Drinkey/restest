from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="restest",
    version="0.0.1",
    author="Junkai Zhang",
    author_email="drink3y@gmail.com",
    description="Simple RESTFul API Test Framework for learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Drinkey/restest",
    packages=find_packages(include=['restest.*']),
    package_dir = {'':'restest'}, 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    
)