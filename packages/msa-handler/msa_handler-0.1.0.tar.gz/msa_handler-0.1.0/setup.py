from setuptools import setup, find_packages

setup(
    name="msa_handler",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["biopython"],
    author="Amin Akbari",
    author_email="akbari.amin7@gmail.com",
    description="Tool for handling MSA files and mapping residue ids",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aminkvh",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
