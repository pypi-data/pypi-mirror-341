from setuptools import setup, find_packages

setup(
    name="BR23021UNO",
    version="1.2.1",
    author="Joyser Leonel Barrera Romero",
    description="Librería para resolver sistemas de ecuaciones lineales y no lineales.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
