from setuptools import setup, find_packages

setup(
    name="AA23028UNO",
    version="0.1.0",
    description="Librería de métodos numéricos para sistemas de ecuaciones lineales y no lineales",
    author="Alexis Aldana",
    packages=find_packages(),
    install_requires=["numpy", "scipy"],
    python_requires=">=3.7",
    license="MIT",
    url="https://pypi.org/project/AA23028UNO/",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
)
