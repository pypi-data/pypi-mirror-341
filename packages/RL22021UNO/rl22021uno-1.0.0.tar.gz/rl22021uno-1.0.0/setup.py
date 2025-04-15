from setuptools import setup, find_packages

setup(
    name="RL22021UNO",
    version="1.0.0",
    author="Mirna Rivas",
    author_email="mirnarivas860@gmail.com",
    description="Librería para resolver sistemas de ecuaciones lineales y no lineales",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Mirna1111/RL22021UNO",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy"
    ],
)

