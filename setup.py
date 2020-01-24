from os import path

from setuptools import setup, find_packages

from pymongo_inmemory import __version__


here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md")) as f:
    long_description = f.read()

required = ["setuptools", "pymongo"]
keywords = ["mongodb", "testing", "pymongo"]

setup(
    name="pymongo_inmemory",
    version=".".join(__version__),
    description="A mongo mocking library with an ephemeral MongoDB running in memory.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kaizendorks/pymongo_inmemory",
    author="Kaizen Dorks",
    author_email="kaizendorks@gmail.com",
    license="MIT",
    packages=find_packages(exclude=["tests", "tests.*", ".vscode"]),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
    ],
    keywords=" ".join(keywords),
    python_requires=">=3.4",
    project_urls={
        "Bug Reports": "https://github.com/kaizendorks/pymongo_inmemory/issues",
        "Source": "https://github.com/kaizendorks/pymongo_inmemory",
    },
)
