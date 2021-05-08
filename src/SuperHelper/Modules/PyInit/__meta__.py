BaseCoverageConfig = """
[run]
branch = True
source = src/

[report]
exclude_lines =
    if self.debug:
    if debug:
    pragma: no cover
ignore_errors = True
"""

BaseGitIgnore = """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# PyCharm
.idea/
"""

BaseTravisConfig = """
os: linux
dist: xenial
python: 3.9
language: python
before_install:
  - python3 --version
  - python3 -m pip install --upgrade pip
install:
  - pip3 install -r requirements.txt
script: make test
after_success: bash <(curl -s https://codecov.io/bash)
"""

BaseCodecovConfig = """
codecov:
  branch: main
  require_ci_to_pass: true

coverage:
  precision: 2
  round: nearest

parsers:
  gcov:
    branch_detection:
      conditional: yes
      loop: yes
      method: no
      macro: no

comment:
  layout: "reach,diff,flags,files,footer"
  behavior: default
  require_changes: false
"""

BaseMakefile = r"""
venv:
	python3 -m venv .venv
	./.venv/bin/pip3 install -r requirements.txt

build:
	python3 setup.py sdist bdist_wheel

publish: build
	twine check dist/* && twine upload dist/*

dev-install:
	pip3 install -e .

test:
	pytest --cov

clean:
	rm -rf build/ dist/ .coverage
	find . -type d -name __pycache__ -exec rm -r {} \*
"""

BaseRequirements = """
wheel
twine
pytest
setuptools
pytest-cov
"""

BaseSetup = """
from setuptools import find_packages, setup

with open("README.md") as fp:
    long_desc = fp.read()

setup(
    name="{}",
    version="0.0.0",
    author="{}",
    author_email="{}",
    description="{},
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="",
    project_urls={
    },
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.6",
)
"""

BaseLicense = """
MIT License

Copyright (c) {} {}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

BaseReadme = """
# {}

{}
"""
