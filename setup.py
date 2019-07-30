from setuptools import setup, find_packages

from pymongo_inmemory import __version__

required = [
    "setuptools", "pymongo"
]

setup(
    name="pymongo_inmemory",
    version=".".join(__version__),
    description="Pymongo Mocking Tool with in memory MongoDB running.",
    author="Kaizen Dorks",
    author_email="kaizendorks@gmail.com",
    license="MIT",
    packages=find_packages(exclude=["tests", "tests.*", ".vscode"]),
    install_requires=required
)
