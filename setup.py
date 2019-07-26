from distutils import find_packages, setup

from pymongo_inmemory import __version__

required = [
    "pymongo"
]

setup(
    name="pymongo_inmemory",
    version=".".join(__version__),
    description="Pymongo Mocking Tool with in memory MongoDB running.",
    author="Kaizen Dorks",
    author_email="kaizendorks@gmail.com",
    license="MIT"
)
