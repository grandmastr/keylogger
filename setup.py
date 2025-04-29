"""
Setup script for the keylogger package.
"""

from setuptools import setup, find_packages

setup(
    name="keylogger",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pynput>=1.7.6",
    ],
    author="grandmastr",
    author_email="",
    description="A simple keylogger package for recording keyboard inputs",
    long_description=open("README.md").read() if hasattr(__builtins__, 'open') else "",
    long_description_content_type="text/markdown",
    keywords="keylogger, keyboard, input",
    url="https://github.com/grandmastr/keylogger",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "keylogger=keylogger.keylogger:main",
        ],
    },
)
