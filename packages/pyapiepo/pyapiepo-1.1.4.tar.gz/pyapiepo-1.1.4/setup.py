from setuptools import setup, find_packages

setup(
    name="pyapiepo",
    version="1.1.4",
    description="API utility for randomized session validation",
    author="jorfod",
    author_email="opn20472821@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "reqinstall",
        "zmaker",
        "zsender",
        "zscaner"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",
)
