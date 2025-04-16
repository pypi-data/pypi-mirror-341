from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="gadopenapiconverter",
    version="0.0.2",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "gadopenapiconverter=gadopenapiconverter.cli:app",
        ],
    },
    author="Alexander Grishchenko",
    author_email="alexanderdemure@gmail.com",
    description="A CLI tool that generates HTTP clients from an OpenAPI specification",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AlexDemure/gadopenapiconverter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)