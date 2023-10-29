from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="logging_profcomff",
    version="2023.10.29",
    author="Semyon Grigoriev",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/profcomff/logging-lib",
    packages=find_packages(),
    install_requires=["setuptools"],
    classifiers=[
        "Programming Language :: Python :: 3.11",
    ],
)
