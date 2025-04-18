from setuptools import setup, find_packages

setup(
    name="reqinstall",
    version="1.1.0",
    description="A simple utility that automatically installs the requests library",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="roodom",
    author_email="opn3054677@gmail.com",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
