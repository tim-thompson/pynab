import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="Pynab",
    version="0.0.1",
    description="Python wrapper for YNAB API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tim-thompson/pynab",
    author="Tim Thompson",
    author_email="me@tim-thompson.co.uk",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pynab"],
    include_package_data=True,
    install_requires=["requests"],
)
