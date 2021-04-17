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
	rm -rf .test_dir && mkdir .test_dir
	export SUPER_HELPER_APP_DIR=./.test_dir && pytest --cov

docs:
	pdoc --html --force src/SuperHelper

clean-all: clean clean-cfg clean-test

clean:
	pip3 uninstall -y SuperHelper && rm -rf src/*.egg-info
	rm -rf build/ dist/ .coverage
	find . -type d -name __pycache__ -exec rm -r {} \+

clean-cfg:
	rm -rf ~/Library/Application\ Support/SuperHelper/ ~/.config/SuperHelper

clean-test:
	rm -rf .test_dir .pytest_cache coverage.xml .coverage
	rm -rf .coverage.*
