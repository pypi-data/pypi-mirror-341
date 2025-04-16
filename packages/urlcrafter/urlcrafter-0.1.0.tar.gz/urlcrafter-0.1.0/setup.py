from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="urlcrafter",
    version="0.1.0",
    author="Madhav Panchal",
    author_email="madhavpanchal1716@gmail.com",
    description="A human-friendly library for building and manipulating URLs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Madhav1716/URLCrafter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords="url, http, api, rest, web, urlbuilder, parsing",
)
