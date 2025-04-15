from setuptools import setup, find_packages

setup(
    name="PA23013UNO",
    version="1.0.0",
    author="Emerson Ponce",
    description="Librería para resolver sistemas de ecuaciones lineales y no lineales.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)