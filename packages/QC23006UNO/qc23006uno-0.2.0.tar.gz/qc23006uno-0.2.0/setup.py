from setuptools import setup, find_packages

setup(
    name="QC23006UNO",
    version="0.2.0",
    author="Alexandra Quinteros",
    author_email="QC23006@ues.edu.sv",
    description="Librería de sistemas de ecuaciones lineales y no lineales",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tuusuario/GG14054UNO",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "scipy",
    ],
)