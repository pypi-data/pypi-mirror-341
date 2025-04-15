from setuptools import setup, find_packages

setup(
    name="CDA_corto1",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.20.0',
    ],
    author="Fabio Leiva",
    author_email="LT22004@ues.edu.sv",
    description="Librería para resolver sistemas de ecuaciones lineales y no lineales",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/drumsplease-fab/CDA_corto1",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)