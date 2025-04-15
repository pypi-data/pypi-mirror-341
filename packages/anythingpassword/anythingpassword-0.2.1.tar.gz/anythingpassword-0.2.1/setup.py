from setuptools import setup, find_packages

setup(
    name="anythingpassword",
    version="0.2.1",
    packages=find_packages(),
    install_requires=[
        "cryptography==44.0.2",
    ],
    entry_points={
        "console_scripts": [
            "anythingpassword=anythingpassword.cli:cli",
        ],
    },
    author="Akinboye Yusuff",
    author_email="mailakinboye@gmail.com",
    description="This Python application provides a suite of tools for generating, analyzing, encrypting, and managing passwords securely.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/akinboye/anythingpassword",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)