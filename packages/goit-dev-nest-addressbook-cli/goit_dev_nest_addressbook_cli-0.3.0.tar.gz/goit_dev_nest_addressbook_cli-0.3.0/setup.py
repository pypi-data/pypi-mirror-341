from setuptools import setup, find_packages

setup(
    name="goit-dev-nest-addressbook-cli",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        "colorama>=0.4.0",
    ],
    entry_points={
        "console_scripts": [
            "addressbook=addressbook.main:main",
        ],
    },
    python_requires=">=3.8",
    author="Dev Nest",
    description="A simple CLI assistant for managing contacts and notes",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
    ],
)