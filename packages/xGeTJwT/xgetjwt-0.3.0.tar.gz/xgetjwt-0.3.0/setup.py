from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="xGeTJwT",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
        'pycryptodome>=3.10.1',
        'protobuf>=3.20.0'
    ],
    author="BesToPy",
    author_email="abdelkarim@email.com",
    description="JWT Token Generator for Garena API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)