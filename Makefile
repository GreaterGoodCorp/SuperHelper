venv:
	python3 -m venv .venv
	./.venv/bin/pip3 install -r requirements.txt

build:
	python3 setup.py sdist bdist_wheel

publish: build
	twine check dist/* && twine upload dist/*

clean-all: clean clean-cfg

clean: clean-build clean-test

clean-build:
	pip3 uninstall -y SuperHelper && rm -rf src/*.egg-info
	rm -rf build
	rm -rf dist
	find . -type d -name __pycache__ -exec rm -r {} \+

dev-install:
	pip3 install -e .

test:
	pytest --cov=src/SuperHelper

clean-cfg:
	rm -rf ~/Library/Application\ Support/SuperHelper/
	rm -rf ~/.config/SuperHelper

clean-test:
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf .coverage.*
