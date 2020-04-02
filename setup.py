""" Package setup. """

import setuptools

import musicrs

# Requirements
requirements = ["pyodbc>=4.0.27,<5", "flatten_json==0.1.7", "boto3==1.12.6", "youtube-dl==2020.3.24"]

# Development Requirements
requirements_dev = ["pytest==4.*", "mock==3.0.5", "black==19.10b0", "moto==1.3.14"]

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name=musicrs.name,
    version=musicrs.version,
    description="Music recommendation application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    extras_require={"dev": requirements_dev},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
