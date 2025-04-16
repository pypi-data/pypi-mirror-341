from setuptools import setup, find_packages

setup(
    name="binary-fun", # Name on PyPI
    version="0.0.0",
    packages=find_packages(),
    install_requires=[],
    author="Adonis Miclea",
    author_email="tilik_87@yahoo.com",
    description="A Python module that converts and decodes binary.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
