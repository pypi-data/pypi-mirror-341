import os
import sys
from shutil import rmtree
from os.path import dirname, join

from setuptools import setup, Command, find_packages

# Package meta-data.
NAME = "curlformat"
DESCRIPTION = "Convert curl commands to Python HTTP client code"
URL = "https://github.com/ihandmine/curlformat"  # Update with actual URL
EMAIL = "handmine@outlook.com"  # Update with your email
AUTHOR = "handmine"  # Update with your name
REQUIRES_PYTHON = ">=3.7.0"

# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Get the version from the VERSION file
try:
    with open(join(dirname(__file__), "curlformat/VERSION"), "rb") as f:
        old_version = f.read().decode("ascii").strip()
        maxv, midv, minv = [int(v) for v in old_version.split(".")]
        if minv <= 24:
            minv += 1
        else:
            midv += 1
            minv = 0
        VERSION = ".".join([str(v) for v in [maxv, midv, minv]])
        print(f"old version: {old_version}, new version: {VERSION}")
except FileNotFoundError:
    # If VERSION file doesn't exist, create it with initial version
    VERSION = "0.1.0"
    os.makedirs(os.path.dirname(join(dirname(__file__), "curlformat/VERSION")), exist_ok=True)
    with open(join(dirname(__file__), "curlformat/VERSION"), "w") as f:
        f.write(VERSION + "\n")
    print(f"Created VERSION file with initial version: {VERSION}")


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel distribution...")
        os.system("{0} setup.py sdist bdist_wheel".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine...")
        os.system("twine upload dist/*")

        # Update VERSION file with new version
        with open(join(dirname(__file__), "curlformat/VERSION"), "w") as f:
            f.write(VERSION + "\n")

        self.status("git option [add]")
        os.system("git add curlformat/VERSION")

        self.status("git option [commit][push]")
        os.system(f'git commit -m "{VERSION}"')
        os.system("git push")
        sys.exit()


class DevelopCommand(Command):
    """Support setup.py develop."""

    description = "Install the package in development mode."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.status("Installing in development mode...")
        os.system("{0} -m pip install -e .".format(sys.executable))
        self.status("Installation complete!")
        sys.exit()


# Define extras_require for optional dependencies
extras_require = {
    "all": [
        "requests",
        "httpx",
        "aiohttp",
        "pycurl",
        "pyhttpx",
        "curl_cffi",
        "pyperclip"
    ],
    "httpx": ["httpx[http2]>=0.23.0"],
    "aiohttp": ["aiohttp"],
    "pycurl": ["pycurl"],
    "curl_cffi": ["curl_cffi"],
    "pyhttpx": ["pyhttpx"],
    "dev": [
        "pytest",
        "black",
        "isort",
        "mypy",
        "twine",
        "wheel",
        "build"
    ]
}


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    packages=find_packages(include=["curlformat", "curlformat.*"]),
    include_package_data=True,
    package_data={
        "curlformat": ["VERSION", "*.py", "*.tmpl", "*.cfg"]
    },
    install_requires=[
        "requests>=2.25.0",
        "pyperclip>=1.8.0",
        "six>=1.15.0"
    ],
    extras_require=extras_require,
    entry_points={
        "console_scripts": ["curlformat = curlformat.bin:main"]
    },
    python_requires=REQUIRES_PYTHON,
    license="MIT",
    keywords="""
        curl
        requests
        httpx
        aiohttp
        pycurl
        curl_cffi
        http
        converter
        python3
    """,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Operating System :: OS Independent",
    ],
    cmdclass={
        "upload": UploadCommand,
        "develop": DevelopCommand
    },
    zip_safe=False,
)
