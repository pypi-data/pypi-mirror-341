from setuptools import setup, find_packages

setup(
    name="MR22142UNO",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["numpy", "scipy"],
    author="Andrea Lisbeth Martinez Ramirez",
    author_email="mr22142@ues.edu.sv",
    description="Librería para resolver sistemas de ecuaciones lineales y no lineales",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Martinez-Ramirez-Andrea/MR22142UNO",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
