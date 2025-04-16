from setuptools import setup, find_packages

setup(
    name="password-fun", # Name on PyPI
    version="0.0.0",
    packages=find_packages(),
    install_requires=[],
    author="Adonis Miclea",
    author_email="tilik_87@yahoo.com",
    description="A simple Python module that generates, checks vulnerability, and other. Recommended for programmers who likes playing with passwords.",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
