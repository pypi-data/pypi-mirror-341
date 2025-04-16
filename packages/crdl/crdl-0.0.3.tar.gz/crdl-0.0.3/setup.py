from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

meta = {}
with open("./crunchyroll/version.py", encoding="utf-8") as f:
    exec(f.read(), meta)

setup(
    name="crdl",
    version=meta["__version__"],
    author="TanmoyTheBoT",
    author_email="tanmoysarkershuvo@gmail.com",
    description="A simple crunchyroll downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TanmoyTheBoT/Crunchy-Downloader",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests",
        "pywidevine",
        "pathlib",
        "setuptools",
    ],
    entry_points={
        "console_scripts": [
            "crdl=crunchyroll.cli:main",
        ],
    },

) 