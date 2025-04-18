from setuptools import setup, find_packages

setup(
    name="gpushare",
    version="0.1.11",
    description="Client library for the GPU Share service",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sriman Yalavarthi",
    url="https://github.com/Srimany123/gpushare",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
