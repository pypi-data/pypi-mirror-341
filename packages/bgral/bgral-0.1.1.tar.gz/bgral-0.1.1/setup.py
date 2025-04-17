from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
    
setup(
    name="bgral",
    version="0.1.1",
    author="Bhavya Gujral",
    description="A simple library that tells who made it",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='bhavya.gujral2608@gmail.com',
    url='https://github.com/bhavyagujral26/bgral',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6'
)
