from setuptools import setup, find_packages

setup(
    name="alia-apm",
    version="0.1.1",
    description="A collection of Python scripts by me, Alia. The successor of anpm.",

    author="Alia Normal",
    author_email="dan.driscoll@aussiebb.com",

    packages=find_packages(),

    license="MIT",

    install_requires=[
        "discord > 2.0",
    ],
    python_requires=">=3.12",
)
