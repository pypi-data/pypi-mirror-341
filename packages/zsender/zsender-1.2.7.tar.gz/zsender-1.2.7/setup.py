from setuptools import setup, find_packages

setup(
    name="zsender",
    version="1.2.7",
    description="A system for sending data via POST request with client-side uniqueness control",
    author="foofro",
    author_email="opn5726634@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "reqinstall"
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
)
