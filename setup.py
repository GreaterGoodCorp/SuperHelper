from setuptools import setup, find_packages

with open("README.md") as fp:
    long_desc = fp.read()

exec(open("src/SuperHelper/__init__.py").read())

setup(
    name="SuperHelper",
    version=__version__,
    author="Nguyen Thai Binh",
    author_email="binhnt.mdev@gmail.com",
    description="A collection of Python CLI to make life easier for terminal geeks!",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/GreaterGoodCorp/FocusEnabler",
    project_urls={
        "Bug Tracker": "https://github.com/GreaterGoodCorp/FocusEnabler/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Home Automation",
        "Topic :: Office/Business",
        "Topic :: Utilities",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": ["helper = SuperHelper.Core:main_entry"],
    },
    install_requires=[
        "click",
        "colorama",
    ],
    python_requires=">=3.6",
)
